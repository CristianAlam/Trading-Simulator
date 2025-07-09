#PURPOSE: extract trades from the metatradear platform
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

class TradeExtractor:
    def __init__(self, symbol="*US30.cash*", from_date=datetime(2025, 5, 10), to_date=None):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date or datetime.now()
        self.trades_df = None

    def initialize_mt5(self):
        if not mt5.initialize():
            raise ConnectionError(f"MetaTrader 5 initialization failed: {mt5.last_error()}")

    def shutdown_mt5(self):
        mt5.shutdown()

    def fetch_deals(self):
        self.initialize_mt5()
        deals = mt5.history_deals_get(self.from_date, self.to_date, group=self.symbol)
        self.shutdown_mt5()

        if deals is None or len(deals) == 0:
            raise ValueError("No deals found or error occurred.")

        df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def extract_trades(self):
        df = self.fetch_deals()

        entries = df[df['entry'] == 0]
        exits = df[df['entry'] == 1]

        trades = pd.merge(
            entries,
            exits,
            on='position_id',
            suffixes=('_entry', '_exit')
        )

        trade_summary = trades[[
            'position_id',
            'time_entry', 'time_exit',
            'price_entry', 'price_exit',
            'type_entry', 'volume_entry'
        ]].copy()

        trade_summary.rename(columns={
            'time_entry': 'entry_time',
            'time_exit': 'exit_time',
            'price_entry': 'entry_price',
            'price_exit': 'exit_price',
            'type_entry': 'position_type',
            'volume_entry': 'volume'
        }, inplace=True)

        trade_summary['position_type'] = trade_summary['position_type'].map({0: 'buy', 1: 'sell'})

        self.trades_df = trade_summary
        return trade_summary
