from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from auth.connectClient import paperTradingClient, liveTradingClient, dataClient
from datetime import datetime, timezone
import time
import os
import json

class BuyingBot:
    SAVE_FILE = "open_positions.json"
    RESTRICTED_POSITIONS_FILE = "restricted_positions.json"

    def __init__(self):
        pass

    def place_market_order_and_save_to_file(self, symbol, qty=1):

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
            symbols=[symbol],
            order_type=OrderType.TRAILING_STOP
        )
        open_trailing_orders = liveTradingClient.get_orders(filter=order_filter)
        if len(open_trailing_orders) > 0:
            print(f"Open trailing stop order exists for {symbol}, skipping buy to avoid potential day trade.")
            return
    
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        closed_filter = GetOrdersRequest(
            status="closed",
            symbols=[symbol],
            order_type=OrderType.TRAILING_STOP,
            after=start_of_day
        )
        closed_trailing_orders = liveTradingClient.get_orders(filter=closed_filter)
        if len(closed_trailing_orders) > 0:
            print(f"Trailing stop for {symbol} already closed today — skipping buy to avoid PDT.")
            return

        if os.path.exists(self.RESTRICTED_POSITIONS_FILE):
            with open(self.RESTRICTED_POSITIONS_FILE, "r") as f:
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
    
        qty = self.calculate_position_size(buying_power, current_price)

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
            if order_status.status in ["filled"]: #removed "new" from this list
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
            if os.path.exists(self.SAVE_FILE):
                with open(self.SAVE_FILE, "r") as f:
                    positions = json.load(f)
            else:
                positions = []

            positions.append(pos_data)
            with open(self.SAVE_FILE, "w") as f:
                json.dump(positions, f, indent=2)
            print(f"Saved positions for {symbol}, will attach trailing stop tomorrow.")

    def calculate_position_size(self, buying_power, share_price, stop_pct=0.04, risk_pct=0.05, bp_fraction=0.18):
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

    