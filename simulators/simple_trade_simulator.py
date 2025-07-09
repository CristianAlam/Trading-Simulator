
# Purpose: loads trades from mt5 terminal, simulates them. and recieves data upon them, then exports to csv
from trade_extractor import TradeExtractor
from trade import Trade
from datetime import datetime
import MetaTrader5 as mt5
from price_action.price_data import PriceData
import pandas as pd

# import the price data:
# === Initialize price data access (timeframe is irrelevant since we use ticks) ===
price_data = PriceData("US30.cash", mt5.TIMEFRAME_M1)
# Step 1: Get historical trades from TradeExtractor
extractor = TradeExtractor(from_date=datetime(2025, 5, 10))
trades_df = extractor.extract_trades()


# Step 2: Convert each row to a Trade object
trade_objects = []

for i, row in trades_df.iterrows():
    trade = Trade(
        index=i + 1,
        trade_type=row['position_type'],
        open_time=row['entry_time'],
        close_time=row['exit_time'],
        open_price=row['entry_price'],
        close_price=row['exit_price'],
        position_size = row['volume']
    )
    # Optionally: attach tick data and analyze (if available later)
    df_ticks = price_data.load_ticks_range(trade.open_time, trade.close_time)
    trade.attach_ticks(df_ticks)

    trade_objects.append(trade)


columns = [
    "Date", "Day", "Asset", "Trade Type", "Open Time", "Close Time", "Duration","Position Size", "Profit (pts)",
    "Max DD", "Max DD time", "Won - could it be more profitable ?", "Lost - could it loose less?",
     "Description"
]

rows = []

# Step 3: Print trade summaries
for trade in trade_objects:
    trade.analyze()
    row = {
        "Date": trade.date,
        "Day": trade.day,
        "Asset": "US30.cash",
        "Trade Type": trade.type.upper(),
        "Open Time": trade.open_time.time(),
        "Close Time": trade.close_time.time(),
        "Duration": trade.duration,
        "Position Size": trade.position_size,
        "Profit (pts)": round(trade.pnl, 2) if trade.pnl is not None else "",
        "Max DD": round(trade.max_drawdown, 2) if trade.max_drawdown is not None else "",
        "Max DD time": round(trade.drawdown_time, 1) if trade.drawdown_time is not None else "",
        "Won - could it be more profitable ?": "",
        "Lost - could it loose less?": "",
        "Description": ""
    }
    rows.append(row)
    print(trade.summary())

df_to_export = pd.DataFrame(rows, columns=columns)
df_to_export.to_csv("trades_export.csv", index=False)

