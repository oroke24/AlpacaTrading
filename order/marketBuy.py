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

def place_market_order(symbol, qty=1, side=OrderSide.BUY):
    order = MarketOrderRequest(
        symbol=symbol, 
        qty=qty,
        side=side,
        time_in_force=TimeInForce.GTC
    )
    return paperTradingClient.submit_order