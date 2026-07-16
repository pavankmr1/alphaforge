from paper_trading.order import Order
from paper_trading.paper_broker import PaperBroker


class PositionSizer:
    """
    AlphaForge V4

    Calculates the order quantity based on
    portfolio risk.

    Responsibilities
    ----------------
    - Capital allocation
    - Risk-based sizing

    Does NOT
    ----------
    - Validate orders
    - Execute trades
    """

    def __init__(

        self,

        broker: PaperBroker,

        risk_per_trade: float = 0.01

    ):

        self.broker = broker

        self.risk_per_trade = risk_per_trade

    # ======================================================
    # SIZE ORDER
    # ======================================================

    def size(

        self,

        order: Order

    ) -> Order:

        if order is None:

            return None

        if order.stop_loss is None:

            return order

        risk_amount = (

            self.broker.portfolio_value()

            * self.risk_per_trade

        )

        stop_distance = abs(

            order.price

            - order.stop_loss

        )

        if stop_distance <= 0:

            return order

        quantity = int(

            risk_amount

            / stop_distance

        )

        order.quantity = max(

            quantity,

            1

        )

        return order