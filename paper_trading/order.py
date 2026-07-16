from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    """
    AlphaForge V4

    Represents an order ready to be executed.
    """

    side: str

    quantity: int

    price: float

    order_type: str = "MARKET"

    status: str = "PENDING"

    timestamp: Optional[datetime] = None

    stop_loss: Optional[float] = None

    target: Optional[float] = None