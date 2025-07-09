# purpose: plot the candles that we imported from metatrader

from price_data import PriceData
from datetime import datetime
import MetaTrader5 as mt5
import mplfinance as mpf


# Load and plot candles from multiple timeframes
def plot_candles(symbol, timeframe, tf_name, start, end):
    print(f"--- Plotting {tf_name} candles for {symbol} ---")

    pd_obj = PriceData(symbol, timeframe)
    pd_obj.load_range(start, end)
    df = pd_obj.get_dataframe()

    mpf.plot(df, type='candle', style='charles', title=f"{symbol} - {tf_name}",
             ylabel='Price', volume=False, show_nontrading=False)


# Time range to test
start_time = datetime(2025, 4, 1)
end_time = datetime(2025, 4, 5)

# H1
plot_candles("XAUUSD", mt5.TIMEFRAME_H1, "H1", start_time, end_time)

# H4
plot_candles("XAUUSD", mt5.TIMEFRAME_H4, "H4", start_time, end_time)

# Daily
plot_candles("XAUUSD", mt5.TIMEFRAME_D1, "D1", start_time, end_time)
