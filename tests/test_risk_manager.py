from paper_trading.order import Order
from paper_trading.paper_broker import PaperBroker
from paper_trading.risk_manager import RiskManager


def test_buy_order_approved():

    broker = PaperBroker()

    risk = RiskManager(broker)

    order = Order(

        side="BUY",

        quantity=10,

        price=100

    )

    result = risk.validate(order)

    assert result.approved


def test_duplicate_position_rejected():

    broker = PaperBroker()

    broker.buy(100, 1)

    risk = RiskManager(broker)

    order = Order(

        side="BUY",

        quantity=1,

        price=100

    )

    result = risk.validate(order)

    assert result.approved is False


def test_sell_without_position():

    broker = PaperBroker()

    risk = RiskManager(broker)

    order = Order(

        side="SELL",

        quantity=1,

        price=100

    )

    result = risk.validate(order)

    assert result.approved is False


def test_invalid_quantity():

    broker = PaperBroker()

    risk = RiskManager(broker)

    order = Order(

        side="BUY",

        quantity=0,

        price=100

    )

    result = risk.validate(order)

    assert result.approved is False


def test_insufficient_cash():

    broker = PaperBroker(

        initial_cash=100

    )

    risk = RiskManager(broker)

    order = Order(

        side="BUY",

        quantity=10,

        price=100

    )

    result = risk.validate(order)

    assert result.approved is False