from paper_trading.portfolio import Portfolio
from paper_trading.trade_journal import TradeJournal


class PerformanceAnalytics:
    """
    Computes trading performance statistics from
    the portfolio and trade journal.
    """

    def __init__(
        self,
        portfolio: Portfolio,
        journal: TradeJournal,
    ):
        self.portfolio = portfolio
        self.journal = journal

    # ======================================================
    # TRADE COUNTS
    # ======================================================

    def total_trades(self):
        return len(self.journal.all_trades())

    def winning_trades(self):
        return len(self.journal.winning_trades())

    def losing_trades(self):
        return len(self.journal.losing_trades())

    # ======================================================
    # PROFITABILITY
    # ======================================================

    def gross_profit(self):

        return sum(
            trade.pnl
            for trade in self.journal.winning_trades()
        )

    def gross_loss(self):

        return abs(
            sum(
                trade.pnl
                for trade in self.journal.losing_trades()
            )
        )

    def net_pnl(self):

        return sum(
            trade.pnl
            for trade in self.journal.all_trades()
        )

    def win_rate(self):

        total = self.total_trades()

        if total == 0:
            return 0.0

        return (
            self.winning_trades()
            / total
        ) * 100

    def average_win(self):

        wins = self.winning_trades()

        if wins == 0:
            return 0.0

        return self.gross_profit() / wins


    def average_loss(self):

        losses = self.losing_trades()

        if losses == 0:
            return 0.0

        return self.gross_loss() / losses


    def profit_factor(self):

        gross_loss = self.gross_loss()

        if gross_loss == 0:
            return float("inf")

        return self.gross_profit() / gross_loss


    def expectancy(self):

        total = self.total_trades()

        if total == 0:
            return 0.0

        return self.net_pnl() / total

    def summary(self):

        return {
            "total_trades": self.total_trades(),
            "winning_trades": self.winning_trades(),
            "losing_trades": self.losing_trades(),
            "gross_profit": self.gross_profit(),
            "gross_loss": self.gross_loss(),
            "net_pnl": self.net_pnl(),
            "win_rate": self.win_rate(),
            "average_win": self.average_win(),
            "average_loss": self.average_loss(),
            "profit_factor": self.profit_factor(),
            "expectancy": self.expectancy(),
        }