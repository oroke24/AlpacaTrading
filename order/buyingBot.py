from alpaca.data.requests import StockLatestTradeRequest
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from auth.connectClient import paperTradingClient, liveTradingClient, dataClient
from datetime import datetime, timezone
import yfinance as yf
import numpy as np
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
        five_day_atr = self.get_atr(symbol)

        if(day_trades >= 3):
            print(f"No trading today: Day Trade Count too high ({day_trades}), max allowed: 3")
            return
        
        if(five_day_atr > 13.0):
            print(f"Skipping {symbol}: 5-day ATR threshold exceeded: ({five_day_atr}), max allowed: 13.0%\n")
            return
    
        order_filter = GetOrdersRequest(
            status="open",
            symbols=[symbol],
            order_type=OrderType.TRAILING_STOP
        )
        open_trailing_orders = liveTradingClient.get_orders(filter=order_filter)
        if len(open_trailing_orders) > 0:
            print(f"Open trailing stop order exists for {symbol}, skipping buy to avoid potential day trade.\n")
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
            print(f"Trailing stop for {symbol} already closed today — skipping buy to avoid PDT.\n")
            return

        if os.path.exists(self.RESTRICTED_POSITIONS_FILE):
            with open(self.RESTRICTED_POSITIONS_FILE, "r") as f:
                restricted = json.load(f)
        else:
            restricted = []

        # Skip restricted symbols
        if symbol in restricted:
            print(f"Skipping {symbol}: sold today, cannot rebuy until tomorrow.\n")
            return

        # --- get buying power ---
        buying_power = float(liveTradingClient.get_account().buying_power)

        # --- get share price ---
        latest_quote = dataClient.get_stock_latest_trade(StockLatestTradeRequest(symbol_or_symbols=symbol))
        current_price = latest_quote[symbol].price

        # --- check price to see how many we should order, if any ---
        if current_price >= buying_power:
            print(f"Skipping {symbol}: current price ({current_price}) exceeds buying power ({buying_power})\n")
            return
    
        #qty = self.calculate_position_size(buying_power, current_price)
        qty = self.calculate_position_size(buying_power, current_price)

        if qty == 0:
            print(f"Skipping {symbol}: {current_price}, too risky (qty to buy was 0).\n")
            return
    
        print(f"latest price for {symbol}: {current_price}, so I'm buying {qty}\n")

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
                print(f"Order for {symbol} did not fill, status: {order_status.status}\n")
                break
            timeLimit -= time_interval
            if timeLimit <= 0:
                if order_status.status in ["accepted", "partially_filled"]:
                    print(f"Cancelling stuck order for {symbol}, status: {order_status.status}\n")
                    liveTradingClient.cancel_order_by_id(buy_order.id)
                else:
                    print(f"Time limit exceeded, buy order for {symbol} not filled..\n")
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
            print(f"Saved positions for {symbol}, will attach trailing stop tomorrow.\n")

    def calculate_position_size(self, buying_power, share_price, stop_pct=0.04, risk_pct=0.05, bp_fraction=0.18):
        """
        Calculate number of shares to buy based on risk management and capital constraints.
        Returns: quantity of shares_to_buy.
        """
        try:
            # Validate inputs
            if share_price <= 0:
                print("Invalid share price. Must be > 0.")
                return 0
            if not (0 < stop_pct < 1) or not (0 < risk_pct < 1) or not (0 < bp_fraction <= 1):
                print("Percent parameters must be between 0 and 1.")
                return 0

            # Effective capital allocation for this trade
            effective_bp = buying_power * bp_fraction
        
            # Maximum dollar amount willing to risk on this trade
            risk_amount = effective_bp * risk_pct
        
            # Dollar risk per share based on stop loss distance
            stop_distance = share_price * stop_pct
            if stop_distance == 0:
                print("Stop loss distance cannot be zero.")
                return 0
        
            # Number of shares constrained by risk per trade
            shares_risk = int(risk_amount // stop_distance)
        
            # Number of shares affordable within allocated buying power
            shares_affordable = int(effective_bp // share_price)
        
            # Final shares to buy is minimum of risk-based and affordable shares
            shares_to_buy = min(shares_risk, shares_affordable)
        
            return shares_to_buy if shares_to_buy > 0 else 0

        except Exception as e:
            print(f"Error calculating position size: {e}")
            return 0


    def get_atr(self, symbol, period=5, default_pct=3.5, min_pct=0, max_pct=25):
        """
        Returns a safe trailing stop % for Alpaca orders.
    
        - Calculates ATR as % of price
        - Falls back to default if ATR can't be calculated
        - Clamps the result between min_pct and max_pct
        """
        atr_percent = default_pct  # start with fallback
    
        try:
            df = yf.download(symbol, period="1mo", auto_adjust=True)
            if len(df) > period:
                df['H-L'] = df['High'] - df['Low']
                df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
                df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
                df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1)
                df['ATR'] = df['TR'].rolling(window=period).mean()
            
                latest_atr = df['ATR'].iloc[-1].item()   # force scalar
                price = df['Close'].iloc[-1].item()      # force scalar

                if not np.isnan(latest_atr) and price > 0:
                    atr_percent = (latest_atr / price) * 100
                # Debug info
                print(f"[{symbol}] Price={price:.2f}, ATR={latest_atr:.4f}, Raw%={(latest_atr/price)*100:.2f}")

        except Exception as e:
            print(f"ATR calculation failed for {symbol}, using default {default_pct}%: {e}")
            pass
    
        # Clamp between min and max
        atr_percent = max(min_pct, min(max_pct, atr_percent))
        rounded_atr_percent = round(atr_percent, 2)
        print(f"[{symbol}] Final calculated 5 day atr % (rounded) = {rounded_atr_percent}")
    
        return rounded_atr_percent


    