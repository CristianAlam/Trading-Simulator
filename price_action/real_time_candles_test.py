# Purpose: loads candles in real time
from price_data import PriceData
from datetime import datetime, timedelta
import MetaTrader5 as mt5
import pandas as pd
import time

symbol = "BTCUSD"  # Make sure this matches your broker's symbol
timeframe = mt5.TIMEFRAME_M1

# Step 1: Load historical candles using PriceData
start = datetime.now() - timedelta(hours=1)
end = datetime.now()

pd_m1 = PriceData(symbol=symbol, timeframe=timeframe)
pd_m1.load_range(start=start, end=end)
df = pd_m1.get_dataframe()
print("Initial DataFrame loaded:")
print(df.tail())

# Step 2: Ensure symbol is selected in MT5
if not mt5.initialize():
    print("MT5 initialize failed")
    quit()

if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol {symbol}")
    quit()

# Step 3: Monitor new M1 candles
print(f"\nStarting real-time M1 candle monitoring for {symbol}...")
last_time = df.index[-1]

while True:
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
    if candles is not None and len(candles) > 0:
        candle = candles[0]
        time_dt = datetime.fromtimestamp(candle['time'])

        # Only act on new candles
        if time_dt > last_time:
            print(f"\nNew M1 Candle Closed at {time_dt}")
            print(f"Open:   {candle['open']}")
            print(f"High:   {candle['high']}")
            print(f"Low:    {candle['low']}")
            print(f"Close:  {candle['close']}")
            print(f"Volume: {candle['tick_volume']}")

            # Optional: append new candle to df
            new_row = pd.DataFrame([{
                "open": candle['open'],
                "high": candle['high'],
                "low": candle['low'],
                "close": candle['close'],
                "tick_volume": candle['tick_volume'],
                "spread": candle['spread'],
                "real_volume": candle['real_volume']
            }], index=[time_dt])
            df = pd.concat([df, new_row])
            last_time = time_dt

    else:
        print("No candle data received. Retrying in 5 seconds...")

    time.sleep(5)

