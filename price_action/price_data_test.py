# purpose: tests the priceData class

from price_data import PriceData
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
# Ensure all columns and rows are visible
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 1000)  # Prevent line wrapping
pd.set_option("display.max_rows", None)  # Show all rows (optional)

# Example: Load XAUUSD H1 candles
price_data_h1 = PriceData("XAUUSD", mt5.TIMEFRAME_H1)
price_data_h1.load_range(datetime(2025, 3, 28, 3), datetime(2025, 3, 29, 3))

df = price_data_h1.get_dataframe()
print(df)

# Example: Load XAUUSD D1 candles
price_data_d1 = PriceData("XAUUSD", mt5.TIMEFRAME_D1)
price_data_d1.load_range(datetime(2025, 3, 1, 0), datetime(2025, 4, 1, 0))

df_h1 = price_data_h1.get_dataframe()
print(df_h1)

df_d1 = price_data_d1.get_dataframe()
print(df_d1)

