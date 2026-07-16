from dataclasses import dataclass

from paper_trading.execution_engine import ExecutionEngine
from paper_trading.paper_broker import PaperBroker
from paper_trading.paper_trading_engine import PaperTradingEngine
from paper_trading.risk_manager import RiskManager
from paper_trading.trade_journal import TradeJournal
@dataclass
class DummySignal:

    direction: str

    entry_price: float

    quantity: int = 1


class DummyStrategy:

    def __init__(self):

        self.count = 0

    def on_candle(self, candle):

        self.count += 1

        if self.count == 1:

            return DummySignal(

                "BUY",

                100,

                10

            )

        if self.count == 2:

            return DummySignal(

                "SELL",

                110,

                10

            )

        return None


def test_paper_trading():

    broker = PaperBroker()

    risk = RiskManager(broker)

    journal = TradeJournal()

    engine = ExecutionEngine(

        broker,

        risk,

        journal

    )

    strategy = DummyStrategy()

    trader = PaperTradingEngine(

        strategy,

        engine

    )

    trader.run(

        [1, 2, 3]

    )

    assert broker.realized_pnl() == 100

    assert len(trader.execution_log) == 3