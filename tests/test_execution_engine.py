from dataclasses import dataclass

import pytest

from paper_trading.execution_engine import ExecutionEngine
from paper_trading.order_builder import OrderBuilder
from paper_trading.paper_broker import PaperBroker
from paper_trading.risk_manager import RiskManager
from paper_trading.trade_journal import TradeJournal

journal = TradeJournal()
@dataclass
class DummySignal:

    direction: str

    entry_price: float

    quantity: int = 1


def test_buy_execution():

    broker = PaperBroker()

    risk = RiskManager(broker)

    journal = TradeJournal()

    engine = ExecutionEngine(

        broker,

        risk,

        journal

    )
    builder = OrderBuilder()

    signal = DummySignal(
        direction="BUY",
        entry_price=100,
        quantity=10,
    )

    order = builder.build(signal)
    result = engine.execute(order)

    assert result.success
    assert broker.has_position()


def test_sell_execution():

    broker = PaperBroker()

    risk = RiskManager(broker)

    journal = TradeJournal()

    engine = ExecutionEngine(

        broker,

        risk,

        journal

    )

    builder = OrderBuilder()

    buy_order = builder.build(

        DummySignal(

            "BUY",

            100,

            5

        )

    )

    engine.execute(buy_order)

    sell_order = builder.build(

        DummySignal(

            "SELL",

            120,

            5

        )

    )

    result = engine.execute(sell_order)

    assert result.success

    assert broker.has_position() is False

    assert broker.realized_pnl() == 100

    assert len(journal) == 1

def test_invalid_signal_direction():

    builder = OrderBuilder()

    with pytest.raises(ValueError):

        builder.build(

            DummySignal(

                "ABC",

                100

            )

        )


def test_none_signal():

    broker = PaperBroker()

    risk = RiskManager(broker)

    journal = TradeJournal()

    engine = ExecutionEngine(

        broker,

        risk,

        journal

    )

    result = engine.execute(None)

    assert result.success is False