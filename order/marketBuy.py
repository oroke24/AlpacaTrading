from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.requests import MarketOrderRequest, TrailingStopOrderRequest 
from alpaca.trading.enums import OrderSide, TimeInForce, PositionSide
from auth.connectClient import paperTradingClient, liveTradingClient, dataClient
import time
import os
import json

SAVE_FILE = "open_positions.json"

def place_market_order_and_save_to_file(symbol, qty=1):

    # --- get buying power ---
    buying_power = float(liveTradingClient.get_account().buying_power)

    # --- get share price ---
    latest_quote = dataClient.get_stock_latest_trade(StockLatestTradeRequest(symbol_or_symbols=symbol))
    current_price = latest_quote[symbol].price

    # --- check price to see how many we should order, if any ---
    if current_price >= buying_power:
        print(f"Skipping {symbol}: current price ({current_price}) exceeds buying power ({buying_power})")
        return
    
    qty = calculate_position_size(buying_power, current_price)

    if qty == 0:
        print(f"Skipping {symbol}: {current_price}, too risky.")
        return

    
    print(f"latest price for {symbol}: {current_price}, so I'm buying {qty}")

    # --- Make order ---
    order = MarketOrderRequest(
        symbol=symbol, 
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )

    # --- Submit order and wait ---
    buy_order = liveTradingClient.submit_order(order_data=order)
    print(f"Buy order submitted. ID: {buy_order.id}")

    print(f"Waiting for {symbol} buy order to fill...")
    filled = False
    timeLimit = 16
    time_interval = 2 #seconds
    while not filled:
        order_status = liveTradingClient.get_order_by_id(buy_order.id)
        if order_status.status in ["filled"]:
            print(f"order status: {order_status.status}")
            filled = True
        elif order_status.status in ["cancelled", "rejected", "done_for_day"]:
            print(f"Order for {symbol} did not fill, status: {order_status.status}")
            break
        timeLimit -= time_interval
        if timeLimit <= 0:
            if order_status.status in ["accepted", "partially_filled"]:
                print(f"Cancelling stuck order for {symbol}, status: {order_status.status}")
                liveTradingClient.cancel_order_by_id(buy_order.id)
            else:
                print(f"Time limit exceeded, buy order for {symbol} not filled..")
            break
        time.sleep(time_interval)
    # if filled, save this position to JSON file for tomorrows run

    if (filled): 
        pos_data = {"symbol": symbol, "qty": qty}
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                positions = json.load(f)
        else:
            positions = []
        positions.append(pos_data)
        with open(SAVE_FILE, "w") as f:
            json.dump(positions, f, indent=2)
        print(f"Saved positions for {symbol}, will attach trailing stop tomorrow.")


def place_trailing_stops_from_local_file(trail_percent=8.0):
    if not os.path.exists(SAVE_FILE):
        print("No saved positions from yesterday.")
        return

    with open(SAVE_FILE, "r") as f:
        positions = json.load(f)

    remaining_positions = []
    for pos in positions:
        symbol = pos["symbol"]
        qty = pos["qty"]

        try:
            trailing_stop_order = TrailingStopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                trail_percent=float(trail_percent),
                time_in_force=TimeInForce.GTC
            )

            sell_order = liveTradingClient.submit_order(order_data=trailing_stop_order)
            print(f"Trailing stop sell for {symbol} submitted. ID: {sell_order.id}")

        except Exception as e:
            print(f"Failed to submit trailing stop for {symbol}: {e}")
            remaining_positions.append(pos)

    # Only clear positions that succeeded
    if remaining_positions:
        with open(SAVE_FILE, "w") as f:
            json.dump(remaining_positions, f, indent=2)
    else:
        os.remove(SAVE_FILE)

def calculate_position_size(buying_power, share_price, stop_pct=0.08, risk_pct=0.05):
    try:
        risk_amount = buying_power * risk_pct
        stop_distance = share_price * stop_pct
        shares_to_buy = int(risk_amount // stop_distance)
        #print(f"buying_power: {buying_power}, risk_amount: {risk_amount}, share_price: {share_price}, stop_distance: {stop_distance} -- shares_to_buy: {shares_to_buy}")
        return shares_to_buy if shares_to_buy > 0 else 0

    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 1


'''
# ----- OLD FUNCTIONS -----
def place_trailing_stop_buy(symbol, qty=1, trail_percent=5):
    # --- check price to see how many we should order ---
    latest_quote = dataClient.get_stock_latest_trade(StockLatestTradeRequest(symbol_or_symbols=symbol))
    current_price = latest_quote[symbol].price
    #base case, don't order any stocks under .05 
    if(current_price < .05):
        print(f"{current_price} is too low to trust. Skipping {symbol}") 
        return
    elif(current_price < .10): qty = 10
    elif(current_price < .50): qty = 5
    elif(current_price < 1): qty = 2

    # --- continue with order --- 

    order = TrailingStopOrderRequest(
        symbol=symbol, 
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC,
        trail_percent=float(trail_percent)
    )

    buy_order = liveTradingClient.submit_order(order_data=order)
    print(f"Buy order submitted. ID: {buy_order.id}")

    print(f"Waiting for {symbol} buy order to fill...")
    filled = False
    timeLimit = 15
    while not filled:
        order_status = liveTradingClient.get_order_by_id(buy_order.id)
        if order_status.status == "filled":
            filled = True
        if timeLimit <= 0:
            # filled = False
            print(f"time limit exceeded, buy order for {symbol} not filled..")
            break
        else:
            time.sleep(1)
            timeLimit -= 1
    # if filled, save this position to JSON for tomorrows run
    if (filled): 
        pos_data = {"symbol": symbol, "qty": qty}
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                positions = json.load(f)
        else:
            positions = []
        positions.append(pos_data)
        with open(SAVE_FILE, "w") as f:
            json.dump(positions, f, indent=2)
        print(f"Saved positions for {symbol}, will attach trailing stop tomorrow.")

def place_market_order_with_trailing_percentage(symbol, qty=1, trail_percent=1.0):
    order = MarketOrderRequest(
        symbol=symbol, 
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )

    buy_order = liveTradingClient.submit_order(order_data=order)
    print(f"Buy order submitted. ID: {buy_order.id}")

    print(f"Waiting for {symbol} buy order to fill...")
    filled = False
    timeLimit = 15
    while not filled:
        order_status = liveTradingClient.get_order_by_id(buy_order.id)
        if order_status.status == "filled":
            filled = True
        if timeLimit <= 0:
            # filled = False
            print(f"time limit exceeded, buy order for {symbol} not filled..")
            break
        else:
            time.sleep(1)
            timeLimit -= 1
    if (filled): 
        print(f"Buy order filled for {symbol}.")

        trailing_stop_order = TrailingStopOrderRequest(
            symbol = symbol,
            qty = qty,
            side=OrderSide.SELL,
            trail_percent=str(trail_percent),
            time_in_force = TimeInForce.GTC
        )

        sell_order = liveTradingClient.submit_order(order_data=trailing_stop_order)
        print(f"Trailing stop sell order for {symbol} submitted. ID: {sell_order.id}")
'''

