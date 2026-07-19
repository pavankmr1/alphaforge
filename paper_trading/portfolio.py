from paper_trading.paper_broker import PaperBroker
from paper_trading.trade_journal import TradeJournal


class Portfolio:
    """
    Represents the current trading account.

    Acts as a unified interface over the broker,
    position manager and trade journal.
    """

    def __init__(
        self,
        broker: PaperBroker,
        journal: TradeJournal,
    ):
        self.broker = broker
        self.position_manager = broker.position_manager
        self.journal = journal

    def cash(self):
        return self.broker.available_cash()

    def market_value(self):
        return self.position_manager.market_value()

    def total_value(self):
        return (
            self.cash()
            + self.market_value()
        )

    def realized_pnl(self):
        return self.broker.realized_pnl()

    def unrealized_pnl(self):
        return self.position_manager.unrealized_pnl()

    def open_positions(self):
        return self.position_manager.position_count()

    def summary(self):
        return {
            "cash": self.cash(),
            "market_value": self.market_value(),
            "total_value": self.total_value(),
            "realized_pnl": self.realized_pnl(),
            "unrealized_pnl": self.unrealized_pnl(),
            "open_positions": self.open_positions(),
        }