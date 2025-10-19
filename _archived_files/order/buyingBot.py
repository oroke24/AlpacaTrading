'''
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
''' 