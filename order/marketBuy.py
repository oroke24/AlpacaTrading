from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.requests import MarketOrderRequest, TrailingStopOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, PositionSide
from auth.connectClient import paperTradingClient, liveTradingClient, dataClient
import yfinance as yf
import numpy as np
import pandas as pd
import time
import os
import json

SAVE_FILE = "open_positions.json"
RESTRICTED_POSITIONS_FILE = "restricted_positions.json"

def place_market_order_and_save_to_file(symbol, qty=1):

    """
    Place a market buy order for `symbol`, save it to SAVE_FILE, 
    and skip if symbol is in today's restricted list.
    """
    live_account = liveTradingClient.get_account()
    day_trades = int(live_account.daytrade_count)

    if(day_trades >= 3):
        print(f"No trading today: Day Trade Count too high ({day_trades}), max allowed: 3")
        return
    
    order_filter = GetOrdersRequest(
        status="open",
        symbols=[symbol.upper()],
        order_type=OrderType.TRAILING_STOP
    )
    open_trailing_orders = liveTradingClient.get_orders(filter=order_filter)
    if len(open_trailing_orders) > 0:
        print(f"Open trailing stop order exists for {symbol}, skipping buy to avoid potential day trade.")
        return



    if os.path.exists(RESTRICTED_POSITIONS_FILE):
        with open(RESTRICTED_POSITIONS_FILE, "r") as f:
            restricted = json.load(f)
    else:
        restricted = []

    # Skip restricted symbols
    if symbol in restricted:
        print(f"Skipping {symbol}: sold today, cannot rebuy until tomorrow.")
        return
    

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
        if order_status.status in ["filled", "new"]:
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


def place_trailing_stops_from_local_file(trail_percent=4.5):
    if not os.path.exists(SAVE_FILE):
        print("No saved positions from yesterday.")
        check_all_positions_worth_selling_now()
        return

    with open(SAVE_FILE, "r") as f:
        positions = json.load(f)

    remaining_positions = []
    for pos in positions:
        symbol = pos["symbol"]
        qty = pos["qty"]
        trail_percent = get_atr(symbol, default_pct=trail_percent)

        try:
            trailing_stop_order = TrailingStopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                trail_percent=float(trail_percent),
                time_in_force=TimeInForce.GTC
            )

            sell_order = liveTradingClient.submit_order(order_data=trailing_stop_order)
            print(f"Trailing stop sell for {symbol} with a trail percent of {trail_percent} submitted. ID: {sell_order.id}\n")

        except Exception as e:
            print(f"Failed to submit trailing stop for {symbol}: {e}")
            remaining_positions.append(pos)

    # Only clear positions that succeeded
    if remaining_positions:
        with open(SAVE_FILE, "w") as f:
            json.dump(remaining_positions, f, indent=2)
    else:
        os.remove(SAVE_FILE)

    check_all_positions_worth_selling_now()

def check_all_positions_worth_selling_now():
    all_open_positions = liveTradingClient.get_all_positions()
    for position in all_open_positions:
        try:
            worth_selling_now(position.symbol)
        except Exception as e:
            print(f"Error checking if {position.symbol} is worth selling now: {e}")

def calculate_position_size(buying_power, share_price, stop_pct=0.04, risk_pct=0.05, bp_fraction=0.18):
    try:
        # Only allocate a fraction of buying power
        effective_bp = buying_power * bp_fraction

        risk_amount = effective_bp * risk_pct
        stop_distance = share_price * stop_pct

        shares_risk = int(risk_amount // stop_distance) if stop_distance > 0 else 0
        shares_affordable = int(effective_bp // share_price)

        shares_to_buy = min(shares_risk, shares_affordable)
        return shares_to_buy if shares_to_buy > 0 else 0

    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 0
    

def get_atr(symbol, period=14, default_pct=3.5, min_pct=2, max_pct=8):
    """
    Returns a safe trailing stop % for Alpaca orders.
    
    - Calculates ATR as % of price
    - Falls back to default if ATR can't be calculated
    - Clamps the result between min_pct and max_pct
    """
    trail_percent = default_pct  # start with fallback
    
    try:
        df = yf.download(symbol, period="3mo", auto_adjust=True)
        if len(df) > period:
            df['H-L'] = df['High'] - df['Low']
            df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
            df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
            df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1)
            df['ATR'] = df['TR'].rolling(window=period).mean()
            
            latest_atr = df['ATR'].iloc[-1].item()   # force scalar
            price = df['Close'].iloc[-1].item()      # force scalar

            if not np.isnan(latest_atr) and price > 0:
                trail_percent = (latest_atr / price) * 100

            # Debug info
            print(f"[{symbol}] Price={price:.2f}, ATR={latest_atr:.4f}, Raw%={(latest_atr/price)*100:.2f}")

    except Exception as e:
        print(f"ATR calculation failed for {symbol}, using default {default_pct}%: {e}")
    
    # Clamp between min and max
    trail_percent = max(min_pct, min(max_pct, trail_percent))
    rounded_trail_percent = round(trail_percent, 2)
    print(f"[{symbol}] Final trail % = {rounded_trail_percent}")
    
    
    return rounded_trail_percent


def worth_selling_now(symbol, percent_loss_cut=-2.0):
    try:
        position = liveTradingClient.get_open_position(symbol)
    except Exception:
        print(f"No open position found for {symbol}.  Skipping")
        return False
        
    qty = float(position.qty)

    if qty <= 0:
        print(f"Skipping sell for {symbol}: Position qty is {qty}")
        return False

    percent_gain = float(position.unrealized_plpc) * 100
    print(f"{symbol}: {percent_gain:.2f}% gain")

    if percent_gain <= percent_loss_cut:
        try:
            open_orders = liveTradingClient.get_orders(filter=GetOrdersRequest(status="open"))
            for order in open_orders:
                if order.symbol == symbol:
                    print(f"Canceling existing order for {symbol}: {order.id}")
                    liveTradingClient.cancel_order_by_id(order.id)
        except Exception as e:
            print(f"Could not cancel existion orders for {symbol}: {e}")
        
        print(f"Selling {qty} shares of {position.symbol} (percent_gain: {percent_gain}, Threshold exceeded)")
        order = MarketOrderRequest(
            symbol=position.symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force = TimeInForce.DAY
        )
        liveTradingClient.submit_order(order)

        # Add symbol to restricted list
        if os.path.exists(RESTRICTED_POSITIONS_FILE):
            with open(RESTRICTED_POSITIONS_FILE, "r") as f:
                restricted = json.load(f)
        else:
            restricted = []

        if symbol not in restricted:
            restricted.append(symbol)
            with open(RESTRICTED_POSITIONS_FILE, "w") as f:
                json.dump(restricted, f, indent=2)
            print(f"Added {symbol} to restricted list for today.")
        return True
    return False

def safe_load_json(filename, default=None):
    if not os.path.exists(filename):
        return default if default is not None else []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {filename} is empty or corrupt. Resetting file.")
        return default if default is not None else []

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

