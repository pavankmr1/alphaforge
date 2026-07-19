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