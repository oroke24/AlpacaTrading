from alpaca.trading.requests import MarketOrderRequest, TrailingStopOrderRequest 
from alpaca.trading.enums import OrderSide, TimeInForce
from auth.connectClient import paperTradingClient
import time

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
'''

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

def place_market_order_with_trailing_percentage(symbol, qty=1, trail_percent=1.0):
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
    while not filled:
        order_status = paperTradingClient.get_order_by_id(buy_order.id)
        if order_status.status == "filled":
            filled = True
        else:
            time.sleep(1)
    print("Buy order filled.")

    trailing_stop_order = TrailingStopOrderRequest(
        symbol = symbol,
        qty = qty,
        side=OrderSide.SELL,
        trail_percent=str(trail_percent),
        time_in_force = TimeInForce.GTC
    )

    sell_order = paperTradingClient.submit_order(order_data=trailing_stop_order)
    print(f"Trailing stop sell order submitted. ID: {sell_order.id}")


