from dataclasses import dataclass

from paper_trading.order import Order
from paper_trading.paper_broker import PaperBroker


@dataclass
class RiskResult:
    """
    Result of risk validation.
    """

    approved: bool

    reason: str = ""


class RiskManager:
    """
    AlphaForge V4

    Validates whether an order is allowed
    to be executed.

    Responsibilities
    ----------------
    - Position limits
    - Cash validation
    - Quantity validation

    Does NOT:
    - Execute orders
    - Modify orders
    - Calculate indicators
    """

    def __init__(

        self,

        broker: PaperBroker,

        max_open_positions: int = 1

    ):

        self.broker = broker

        self.max_open_positions = max_open_positions

    # ======================================================
    # VALIDATE
    # ======================================================

    def validate(

        self,

        order: Order

    ) -> RiskResult:

        if order is None:

            return RiskResult(

                approved=False,

                reason="No order."

            )

        if order.quantity <= 0:

            return RiskResult(

                approved=False,

                reason="Invalid quantity."

            )

        if (

            order.side == "BUY"

            and self.broker.has_position()
            and self.max_open_positions <= 1

        ):

            return RiskResult(

                approved=False,

                reason="Position already open."

            )

        if (

            order.side == "BUY"

            and order.price * order.quantity

            > self.broker.available_cash()

        ):

            return RiskResult(

                approved=False,

                reason="Insufficient cash."

            )

        if (

            order.side == "SELL"

            and not self.broker.has_position()

        ):

            return RiskResult(

                approved=False,

                reason="No open position."

            )

        return RiskResult(

            approved=True,

            reason="Approved"

        )