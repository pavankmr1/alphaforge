from paper_trading.paper_broker import PaperBroker


def test_buy_sell():

    broker = PaperBroker(

        initial_cash=100000

    )

    broker.buy(

        price=100,

        quantity=10

    )

    assert broker.has_position()

    broker.sell(

        price=120

    )

    assert broker.has_position() is False

    assert broker.realized_pnl() == 200


def test_unrealized():

    broker = PaperBroker()

    broker.buy(

        price=100,

        quantity=5

    )

    assert broker.unrealized_pnl(110) == 50


def test_reset():

    broker = PaperBroker()

    broker.buy(

        100,

        5

    )

    broker.sell(

        110

    )

    broker.reset()

    assert broker.available_cash() == 100000

    assert len(broker.trade_history) == 0


def test_buy_without_cash():

    broker = PaperBroker(

        initial_cash=100

    )

    try:

        broker.buy(

            price=100,

            quantity=2

        )

    except ValueError:

        return

    assert False


def test_sell_without_position():

    broker = PaperBroker()

    try:

        broker.sell(

            100

        )

    except ValueError:

        return

    assert False