from dataclasses import dataclass
from typing import Optional

from paper_trading.paper_broker import PaperBroker

from paper_trading.risk_manager import RiskManager
from paper_trading.trade_journal import (
    TradeJournal,
    TradeRecord,
)
@dataclass
class ExecutionResult:
    """
    Result of an execution request.
    """

    success: bool

    action: str

    message: str


class ExecutionEngine:
    """
    AlphaForge V4

    Executes strategy signals through a broker.

    Responsibilities
    ----------------
    - Validate execution requests
    - Route orders to broker
    - Return execution status

    Does NOT:

    - calculate indicators
    - manage positions
    - perform risk analysis
    """

    def __init__(

        self,

        broker,

        risk_manager,

        journal: TradeJournal

    ):

        self.broker = broker

        self.risk_manager = risk_manager

        self.journal = journal

    # ======================================================
    # EXECUTE
    # ======================================================

    def execute(

        self,

        order

    ) -> ExecutionResult:

        if order is None:

            return ExecutionResult(

                success=False,

                action="NONE",

                message="No Order."

            )
        risk = self.risk_manager.validate(order)

        if not risk.approved:

            return ExecutionResult(

                success=False,

                action=order.side,

                message=risk.reason

            )

        action = order.side.upper()

        if action == "BUY":

            return self.buy(order)

        if action == "SELL":

            return self.sell(order)

        return ExecutionResult(

            success=False,

            action=action,

            message="Unknown action."

        )

    # ======================================================
    # BUY
    # ======================================================

    def buy(

        self,

        order

    ):

        try:

            self.broker.buy(
                price=order.price,
                quantity=order.quantity,
                entry_time=order.timestamp
            )

            return ExecutionResult(

                success=True,

                action="BUY",

                message="Buy executed."

            )

        except Exception as e:

            return ExecutionResult(

                success=False,

                action="BUY",

                message=str(e)

            )

    # ======================================================
    # SELL
    # ======================================================

    def sell(

        self,

        order

    ):

        try:

            trade = self.broker.sell(

                price=order.price

            )
            self.journal.record(

                TradeRecord(

                    strategy="UNKNOWN",

                    symbol="UNKNOWN",

                    side=trade.direction,

                    quantity=trade.quantity,

                    entry_time=None,

                    exit_time=str(order.timestamp),

                    entry_price=trade.entry_price,

                    exit_price=trade.exit_price,

                    pnl=trade.pnl,

                    stop_loss=order.stop_loss,

                    target=order.target

                )

            )

            return ExecutionResult(

                success=True,

                action="SELL",

                message="Sell executed."

            )

        except Exception as e:

            return ExecutionResult(

                success=False,

                action="SELL",

                message=str(e)

            )