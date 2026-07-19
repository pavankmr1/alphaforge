from dataclasses import dataclass
from datetime import datetime


@dataclass
class PortfolioSnapshot:
    """
    Represents the state of the portfolio at a specific point in time.
    """

    timestamp: datetime

    cash: float

    market_value: float

    total_value: float

    realized_pnl: float

    unrealized_pnl: float

    open_positions: int