from paper_trading.position_manager import PositionManager


def test_open_position():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        10

    )

    assert manager.has_position()


def test_update_price():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        10

    )

    manager.update_price(110)

    position = manager.current()

    assert position.current_price == 110

    assert position.highest_price == 110

    assert position.lowest_price == 100


def test_unrealized_pnl():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        5

    )

    manager.update_price(120)

    assert manager.current().unrealized_pnl() == 100


def test_close_position():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        10

    )

    closed = manager.close_position(115)

    assert closed.realized_pnl == 150

    assert manager.has_position() is False


def test_reset():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        10

    )

    manager.reset()

    assert manager.has_position() is False