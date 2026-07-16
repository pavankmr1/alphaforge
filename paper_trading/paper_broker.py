from dataclasses import dataclass
from typing import List

from paper_trading.position_manager import PositionManager


@dataclass
class PaperTrade:
    """
    Represents a completed paper trade.
    """

    direction: str

    entry_price: float

    exit_price: float

    quantity: int

    pnl: float


class PaperBroker:
    """
    AlphaForge V4

    Simulates a broker for paper trading.

    Responsibilities
    ----------------
    - Manage cash
    - Execute buy/sell
    - Track realized PnL
    - Maintain trade history

    Position lifecycle is delegated to PositionManager.
    """

    def __init__(

        self,

        initial_cash: float = 100000

    ):

        self.initial_cash = float(initial_cash)

        self.cash = float(initial_cash)

        self.position_manager = PositionManager()

        self.trade_history: List[PaperTrade] = []

    # ==========================================================
    # STATUS
    # ==========================================================

    def has_position(self):

        return self.position_manager.has_position()
    # ==========================================================
    # PORTFOLIO
    # ==========================================================

    def portfolio_value(self):
        """
        Current portfolio value.

        For now this is simply available cash.

        Later this will include:
        - Cash
        - Unrealized PnL
        - Open positions
        """

        return self.cash
    def available_cash(self):

        return self.cash

    def realized_pnl(self):

        return sum(

            trade.pnl

            for trade in self.trade_history

        )

    # ==========================================================
    # BUY
    # ==========================================================

    def buy(

        self,

        price,

        quantity=1,

        entry_time=None

    ):

        if self.has_position():

            raise ValueError(

                "Position already open."

            )

        cost = price * quantity

        if cost > self.cash:

            raise ValueError(

                "Insufficient cash."

            )

        self.cash -= cost

        self.position_manager.open_position(

            direction="LONG",

            entry_price=price,

            quantity=quantity,

            entry_time=entry_time

        )

    # ==========================================================
    # SELL
    # ==========================================================

    def sell(

        self,

        price

    ):

        if not self.has_position():

            raise ValueError(

                "No open position."

            )

        position = self.position_manager.current()

        proceeds = price * position.quantity

        self.cash += proceeds

        closed = self.position_manager.close_position(

            exit_price=price

        )

        trade = PaperTrade(

            direction=closed.direction,

            entry_price=closed.entry_price,

            exit_price=float(price),

            quantity=closed.quantity,

            pnl=closed.realized_pnl

        )

        self.trade_history.append(trade)

        return trade

    # ==========================================================
    # UNREALIZED
    # ==========================================================

    def unrealized_pnl(

        self,

        current_price

    ):

        if not self.has_position():

            return 0.0

        self.position_manager.update_price(

            current_price

        )

        return (

            self.position_manager

            .current()

            .unrealized_pnl()

        )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.cash = self.initial_cash

        self.position_manager.reset()

        self.trade_history = []

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        print()

        print("=" * 70)

        print("PAPER BROKER")

        print("=" * 70)

        print()

        print(

            "Cash:",

            round(self.cash, 2)

        )

        print(

            "Open Position:",

            self.has_position()

        )

        print(

            "Trades:",

            len(self.trade_history)

        )

        print(

            "Realized PnL:",

            round(

                self.realized_pnl(),

                2

            )

        )