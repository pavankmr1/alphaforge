from paper_trading.order import Order
from paper_trading.paper_broker import PaperBroker
from paper_trading.position_sizer import PositionSizer


def test_position_size():

    broker = PaperBroker(

        initial_cash=100000

    )

    sizer = PositionSizer(

        broker,

        risk_per_trade=0.01

    )

    order = Order(

        side="BUY",

        quantity=1,

        price=100,

        stop_loss=90

    )

    order = sizer.size(order)

    assert order.quantity == 100


def test_no_stop_loss():

    broker = PaperBroker()

    sizer = PositionSizer(broker)

    order = Order(

        side="BUY",

        quantity=5,

        price=100

    )

    order = sizer.size(order)

    assert order.quantity == 5


def test_zero_stop_distance():

    broker = PaperBroker()

    sizer = PositionSizer(broker)

    order = Order(

        side="BUY",

        quantity=5,

        price=100,

        stop_loss=100

    )

    order = sizer.size(order)

    assert order.quantity == 5


def test_none_order():

    broker = PaperBroker()

    sizer = PositionSizer(broker)

    assert sizer.size(None) is None