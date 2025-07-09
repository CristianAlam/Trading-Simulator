# price_data.py
# purpose: responsible for taking candles data from metatrader and creating a panda dataframe from it.
# it works on any time frame that the users asks for
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd


class PriceData:
    def __init__(self, symbol: str, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.df = None  # Will hold your final DataFrame

    def load_range(self, start: datetime, end: datetime):
        # Connect to MetaTrader 5
        if not mt5.initialize():
            raise ConnectionError("Failed to initialize MetaTrader 5.")

        print(f"Loading {self.symbol} candles from {start} to {end}...")

        # Fetch data from MT5
        rates = mt5.copy_rates_range(self.symbol, self.timeframe, start, end)
        mt5.shutdown()

        if rates is None or len(rates) == 0:
            raise ValueError("No data received from MetaTrader 5.")

        # Convert to DataFrame
        df = pd.DataFrame(rates,
                          columns=["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)

        self.df = df
        print(f"Loaded {len(df)} candles.")

    def load_ticks_range(self, start: datetime, end: datetime):
        # Initialize MT5 connection
        if not mt5.initialize():
            raise ConnectionError("Failed to initialize MetaTrader 5.")

        print(f"Loading TICK data for {self.symbol} from {start} to {end}...")

        # Download tick data (COPY_TICKS_ALL = bid, ask, last)
        ticks = mt5.copy_ticks_range(self.symbol, start, end, mt5.COPY_TICKS_ALL)

        # Shutdown connection
        mt5.shutdown()

        if ticks is None or len(ticks) == 0:
            raise ValueError("No tick data received from MetaTrader 5.")

        # Convert to DataFrame
        df = pd.DataFrame(ticks)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)

        print(f"Loaded {len(df)} ticks.")
        return df


    def get_dataframe(self):
        if self.df is None:
            raise ValueError("No data loaded. Call load_range() first.")
        return self.df
