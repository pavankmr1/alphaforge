from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """
    Represents an active paper trading position.
    """

    direction: str

    entry_price: float

    quantity: int

    entry_time: Optional[datetime] = None

    current_price: Optional[float] = None

    highest_price: Optional[float] = None

    lowest_price: Optional[float] = None

    exit_price: Optional[float] = None

    exit_time: Optional[datetime] = None
    realized_pnl: float = 0.0

    def unrealized_pnl(self):

        if self.current_price is None:

            return 0.0

        return (

            self.current_price

            - self.entry_price

        ) * self.quantity