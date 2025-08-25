from alpaca.trading.requests import MarketOrderRequest, TrailingStopOrderRequest 
from alpaca.trading.enums import OrderSide, TimeInForce, PositionSide
from auth.connectClient import paperTradingClient, liveTradingClient
import time
import os
import json

SAVE_FILE = "open_positions.json"

'''
def wait_for_order_fill(client, order_id, timeout=60):
    """Polls the order until it's filled or timeout (in seconds) occurs."""
    start = time.time()
    while time.time() - start < timeout:
        order = client.get_order_by_id(order_id)
        if order.status == 'filled':
            return order
        time.sleep(1)
    raise TimeoutError(f"Order {order_id} was not filled within {timeout} seconds.")

def find_remaining_to_sell_position(symbol, client=liveTradingClient):
    try:
        pos =  client.get_open_position(symbol)
        # if not pos or pos.side != PositionSide.LONG:
        #     return 0
        long_qty = int(pos.qty)
        print(f"long: {pos.qty}")
        open_orders = client.get_orders(status="open", symbol=symbol)
        existing_sell_qty = sum(int(o.qty) for o in open_orders if o.side == OrderSide.SELL)
        remaining_qty = long_qty - existing_sell_qty
        return max(remaining_qty, 0)

    except Exception as e:
        print("Exception: {e}")
        return -1

def list_open_positions(client=liveTradingClient):
    try:
        positions = client.get_all_positions()
        if not positions:
            print("No open positions.")
            return
        
        print("=== Current Open Positions ===")
        for pos in positions:
            print(f"symbol: {pos.symbol}")
            print(f"Qty: {pos.qty}")
            print(f"Side: {pos.side}")
            print(f"Market Value: {pos.market_value}")
            print(f"Cost Basis: {pos.cost_basis}")
            print(f"Unrealized PnL: {pos.unrealized_pl}")
            print("Remaining to sell: ", find_remaining_to_sell_position(pos.symbol))
            print("-" * 30)

    except Exception as e:
        print("Error fethcing positions:", e)

def apply_trailing_stop(symbol, qty=1, trail_percent=1.0):
    # Step 1: Check if symbol has trailing stop, if yes exit function.
    position = paperTradingClient.get_open_position(symbol) or 0
    if position == 0: 
        print("No position on {symbol}")
        return
    # Step 2: Apply trailing stop order. 
    trailing_stop = TrailingStopOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC,
        trail_percent=trail_percent  # e.g., 1.0 means 1%
    )
    paperTradingClient.submit_order(order_data=trailing_stop)

def place_paper_market_order_with_trailing_percentage(symbol, qty=1, trail_percent=1.0):
    order = MarketOrderRequest(
        symbol=symbol, 
        qty=qty,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )

    buy_order = paperTradingClient.submit_order(order_data=order)
    print(f"Buy order submitted. ID: {buy_order.id}")

    print(f"Waiting for buy order to full...")
    filled = False
    timeLimit = 15
    while not filled:
        order_status = paperTradingClient.get_order_by_id(buy_order.id)
        if order_status.status == "filled" or timeLimit <= 0:
            filled = True
        else:
            time.sleep(1)
            timeLimit -= 1
    print("Buy order filled.")

    trailing_stop_order = TrailingStopOrderRequest(
        symbol = symbol,
        qty = qty,
        side=OrderSide.SELL,
        trail_percent=str(trail_percent),
        time_in_force = TimeInForce.GTC
    )

    sell_order = paperTradingClient.submit_order(order_data=trailing_stop_order)
    print(f"Trailing stop sell order submitted. ID: {symbol}: {sell_order.id}")

'''
def place_market_order_with_trailing_percentage(symbol, qty=1):
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

def place_trailing_stops(trail_percent=8.0):
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



'''
# ----- OLD FUNCTIONS -----
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

