from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

import pandas as pd


@dataclass
class TradeRecord:
    """
    AlphaForge V4

    Represents one completed trade.
    """

    strategy: str

    symbol: str

    side: str

    quantity: int

    entry_time: Optional[str]

    exit_time: Optional[str]

    entry_price: float

    exit_price: float

    pnl: float

    stop_loss: Optional[float] = None

    target: Optional[float] = None


class TradeJournal:
    """
    AlphaForge V4

    Stores completed paper trades.

    Responsibilities
    ----------------
    - Record completed trades
    - Return trade history
    - Export history
    """

    def __init__(

        self,

        output_path: str = "experiments/trade_journal.csv"

    ):

        self.output_path = Path(output_path)

        self.trades: List[TradeRecord] = []

    # ======================================================
    # RECORD
    # ======================================================

    def record(

        self,

        trade: TradeRecord

    ):

        self.trades.append(trade)

    # ======================================================
    # DATAFRAME
    # ======================================================

    def dataframe(self):

        return pd.DataFrame(

            [

                asdict(t)

                for t in self.trades

            ]

        )

    # ======================================================
    # SAVE
    # ======================================================

    def save(self):

        df = self.dataframe()

        self.output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        df.to_csv(

            self.output_path,

            index=False

        )

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.trades.clear()

    # ======================================================
    # COUNT
    # ======================================================

    def __len__(self):

        return len(self.trades)
    # ======================================================
    # ALL TRADES
    # ======================================================

    def all_trades(self):
        return self.trades


    # ======================================================
    # WINNING TRADES
    # ======================================================

    def winning_trades(self):
        return [
            trade
            for trade in self.trades
            if trade.pnl > 0
        ]


    # ======================================================
    # LOSING TRADES
    # ======================================================

    def losing_trades(self):
        return [
            trade
            for trade in self.trades
            if trade.pnl < 0
        ]
    # ======================================================
    # EMPTY
    # ======================================================

    def is_empty(self):

        return len(self.trades) == 0