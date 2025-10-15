from alpaca.trading.requests import MarketOrderRequest, TrailingStopOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from auth.connectClient import paperTradingClient, liveTradingClient
import yfinance as yf
import numpy as np
import os
import json


class SellingBot:
    SAVE_FILE = "open_positions.json"
    RESTRICTED_POSITIONS_FILE = "restricted_positions.json"

    def __init__(self):
        pass

    def place_trailing_stops_from_local_file(self, trail_percent=6):
        if not os.path.exists(self.SAVE_FILE):
            print("No saved positions from yesterday.")
            self.check_all_positions_worth_selling_now()
            return

        with open(self.SAVE_FILE, "r") as f:
            positions = json.load(f)

        remaining_positions = []
        for pos in positions:
            symbol = pos["symbol"]
            qty = pos["qty"]

            base_trail = self.get_atr(symbol, default_pct=trail_percent)
            try:
                position = liveTradingClient.get_open_position(symbol)
                percent_gain = float(position.unrealized_plpc) * 100
            except Exception:
                percent_gain = 0 #fallback incase something goes wrong
        
            if percent_gain >= 30:
                final_trail = 2 #Tighten trail if already at 30% gain
            elif percent_gain >= 20:
                final_trail = 3 #Tighten trail if already at 20% gain
            elif percent_gain >= 15:
                final_trail = 4 #Tighten trail if already at 15% gain
            elif percent_gain >= 10:
                final_trail = 5 #Tighten trail if already at 10% gain
            else:
                final_trail = base_trail

            #Final check: making sure atr suggestion isn't loosened
            final_trail = min(final_trail, base_trail)

            try:
                trailing_stop_order = TrailingStopOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=OrderSide.SELL,
                    trail_percent=float(final_trail),
                    time_in_force=TimeInForce.GTC
                )

                sell_order = liveTradingClient.submit_order(order_data=trailing_stop_order)
                print(f"Trailing stop sell for {symbol} with a trail percent of {final_trail} based on percent gain of {percent_gain} submitted. ID: {sell_order.id}\n")

            except Exception as e:
                print(f"Failed to submit trailing stop for {symbol}: {e}")
                remaining_positions.append(pos)

        # Only clear positions that succeeded
        if remaining_positions:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(remaining_positions, f, indent=2)
        else:
            os.remove(self.SAVE_FILE)

        self.check_all_positions_worth_selling_now()

    def check_all_positions_worth_selling_now(self):
        all_open_positions = liveTradingClient.get_all_positions()
        for position in all_open_positions:
            try:
                self.worth_selling_now(position.symbol)
            except Exception as e:
                print(f"Error checking if {position.symbol} is worth selling now: {e}")
    
    def get_atr(self, symbol, period=14, default_pct=3.5, min_pct=2, max_pct=8):
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

    def worth_selling_now(self, symbol, percent_loss_cut=-2.0):
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
            if os.path.exists(self.RESTRICTED_POSITIONS_FILE):
                with open(self.RESTRICTED_POSITIONS_FILE, "r") as f:
                    restricted = json.load(f)
            else:
                restricted = []

            if symbol not in restricted:
                restricted.append(symbol)
                with open(self.RESTRICTED_POSITIONS_FILE, "w") as f:
                    json.dump(restricted, f, indent=2)
                print(f"Added {symbol} to restricted list for today.")
            return True
        return False