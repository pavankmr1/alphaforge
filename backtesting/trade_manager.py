from typing import Optional

from backtesting.models import Trade, TradeSignal, TradeResult


class TradeManager:

    """
    Responsible ONLY for trade lifecycle.

    Strategy decides WHEN to enter.

    TradeManager decides WHEN trade ends.
    """

    def __init__(self):

        self.trade: Optional[Trade] = None

        self.closed_trades = []

    # ==========================================================
    # STATUS
    # ==========================================================

    def has_trade(self):

        return self.trade is not None

    def current_trade(self):

        return self.trade

    # ==========================================================
    # OPEN
    # ==========================================================

    def open_trade(self, signal: TradeSignal):

        if self.trade is not None:

            return False

        self.trade = Trade(

            signal=signal,

            status="OPEN"

        )

        return True

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close_trade(

        self,

        exit_price,

        exit_time,

        reason

    ):

        if self.trade is None:

            return None

        self.trade.status = "CLOSED"

        self.trade.exit_price = exit_price

        self.trade.exit_time = exit_time

        self.trade.reason = reason

        entry = self.trade.signal.entry_price

        stop = self.trade.signal.stop_loss

        risk = entry - stop

        self.trade.pnl = exit_price - entry

        if risk > 0:

            self.trade.rr = (

                exit_price - entry

            ) / risk

        closed_trade = self.trade

        self.closed_trades.append(

            closed_trade

        )

        self.trade = None

        return closed_trade

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(

        self,

        candle

    ):

        if self.trade is None:

            return None

        signal = self.trade.signal

        # --------------------------------------
        # STOP LOSS
        # --------------------------------------

        if candle["Low"] <= signal.stop_loss:

            trade = self.close_trade(

                exit_price=signal.stop_loss,

                exit_time=candle.name,

                reason="STOP"

            )

            return TradeResult(

                exit_time=trade.exit_time,

                exit_price=trade.exit_price,

                pnl=trade.pnl,

                rr=trade.rr,

                reason="STOP"

            )


        # --------------------------------------
        # TARGET
        # --------------------------------------

        if candle["High"] >= signal.target:

            trade = self.close_trade(

                exit_price=signal.target,

                exit_time=candle.name,

                reason="TARGET"

            )

            return TradeResult(

                exit_time=trade.exit_time,

                exit_price=trade.exit_price,

                pnl=trade.pnl,

                rr=trade.rr,

                reason="TARGET"

            )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.trade = None

        self.closed_trades = []

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        print()

        print("=" * 60)

        print("TRADE MANAGER")

        print("=" * 60)

        print()

        print(

            "Closed Trades :",

            len(self.closed_trades)

        )

        if len(self.closed_trades) == 0:

            return

        wins = sum(

            t.pnl > 0

            for t in self.closed_trades

        )

        losses = len(self.closed_trades) - wins

        print(

            "Wins :", wins

        )

        print(

            "Losses :", losses

        )

        print(

            "Win Rate :",

            round(

                wins / len(self.closed_trades),

                4

            )

        )

        avg_rr = sum(

            t.rr

            for t in self.closed_trades

        ) / len(self.closed_trades)

        print(

            "Average RR :",

            round(

                avg_rr,

                2

            )

        )

        total_pnl = sum(

            t.pnl

            for t in self.closed_trades

        )

        print(

            "Total PnL :",

            round(

                total_pnl,

                2

            )

        )