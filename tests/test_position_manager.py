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
def test_market_value():

    manager = PositionManager()

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=10
    )

    manager.update_price(120)

    assert manager.market_value() == 1200.0
def test_unrealized_pnl():

    manager = PositionManager()

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=10
    )

    manager.update_price(120)

    assert manager.unrealized_pnl() == 200.0
def test_position_count():

    manager = PositionManager()

    assert manager.position_count() == 0

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=5
    )

    assert manager.position_count() == 1

    manager.close_position(110)

    assert manager.position_count() == 0
def test_position_metrics_without_position():

    manager = PositionManager()

    assert manager.market_value() == 0.0
    assert manager.unrealized_pnl() == 0.0   
def test_market_value():

    manager = PositionManager()

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=10
    )

    manager.update_price(120)

    assert manager.market_value() == 1200.0
def test_unrealized_pnl():

    manager = PositionManager()

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=10
    )

    manager.update_price(120)

    assert manager.unrealized_pnl() == 200.0
def test_position_count():

    manager = PositionManager()

    assert manager.position_count() == 0

    manager.open_position(
        direction="BUY",
        entry_price=100,
        quantity=5
    )

    assert manager.position_count() == 1

    manager.close_position(110)

    assert manager.position_count() == 0
def test_position_metrics_without_position():

    manager = PositionManager()

    assert manager.market_value() == 0.0
    assert manager.unrealized_pnl() == 0.0
def test_reset():

    manager = PositionManager()

    manager.open_position(

        "LONG",

        100,

        10

    )

    manager.reset()

    assert manager.has_position() is False