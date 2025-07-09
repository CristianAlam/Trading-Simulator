# trade.py
# This module defines a Trade class for storing and analyzing individual trades using tick data

from datetime import datetime
import pandas as pd

class Trade:
    def __init__(self, index, trade_type, open_time, close_time, open_price, close_price,position_size):
        """
        Initialize a Trade object.

        Parameters:
        - index (int): Trade number/index.
        - trade_type (str): 'buy' or 'sell'.
        - open_time (datetime): Trade entry time.
        - close_time (datetime): Trade exit time.
        - open_price (float): Price at entry.
        - close_price (float): Price at exit.
        """
        self.index = index
        self.type = trade_type.lower()
        self.date = open_time.date()
        self.day  =  open_time.strftime("%A")
        self.open_time = open_time
        self.close_time = close_time
        self.open_price = open_price
        self.close_price = close_price
        self.ticks = None
        self.pnl = None
        self.duration = None
        self.max_drawdown = None
        self.drawdown_time = None
        self.position_size = position_size

    def attach_ticks(self, ticks_df):
        """
        Attach tick data to the trade.

        Parameters:
        - ticks_df (pd.DataFrame): DataFrame of tick data.
        """

        # Filter tick data to match trade's time window
        filtered_ticks = ticks_df[
            (ticks_df.index >= self.open_time) &
            (ticks_df.index <= self.close_time)
        ]

        self.ticks = filtered_ticks

    def analyze(self):
        """
        Analyze the trade: compute PnL, duration, and drawdown.
        """
        self.duration = round((self.close_time - self.open_time).total_seconds() / 60, 1)


        # Calculate PnL
        if self.type == 'buy':
            self.pnl = self.close_price - self.open_price
        else:
            self.pnl = self.open_price - self.close_price

        # Calculate drawdown
        if self.ticks is not None and not self.ticks.empty:
            if self.type == 'buy':
                min_bid = self.ticks['bid'].min()
                min_time = self.ticks['bid'].idxmin()
                self.max_drawdown = self.open_price - min_bid
                self.drawdown_time = round((min_time - self.open_time).total_seconds() / 60, 1)
            else:
                max_ask = self.ticks['ask'].max()
                max_time = self.ticks['ask'].idxmax()
                self.max_drawdown = max_ask - self.open_price
                self.drawdown_time = round((max_time - self.open_time).total_seconds() / 60, 1)

    def summary(self):
        """
        Return a formatted string summarizing the trade's analysis.
        """
        pnl_str = f"{self.pnl:.2f}" if self.pnl is not None else "N/A"
        dd_str = f"{self.max_drawdown:.2f}" if self.max_drawdown is not None else "N/A"
        dd_time_str = f"{self.drawdown_time:.1f}min" if self.drawdown_time is not None else "N/A"
        duration_str = f"{self.duration:.1f}min" if self.duration is not None else "N/A"

        return (
            f"Trade {self.index:02} | date: {self.date} | day: {self.day:<9} | "
            f"open: {self.open_time.time()} | close: {self.close_time.time()} | {self.type.upper():<4} | "
            f"PnL: {pnl_str:>7} | Max DD: {dd_str:>7} | Time to DD: {dd_time_str:>7} | Duration: {duration_str:>7} | "
            f"Volume: {self.position_size}"
        )


