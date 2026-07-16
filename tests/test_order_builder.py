from dataclasses import dataclass

import pytest

from paper_trading.order_builder import OrderBuilder


@dataclass
class DummySignal:

    direction: str

    entry_price: float

    quantity: int = 5

    stop_loss: float = 95

    target: float = 110


def test_build_buy_order():

    builder = OrderBuilder()

    order = builder.build(

        DummySignal(

            "BUY",

            100

        )

    )

    assert order.side == "BUY"

    assert order.price == 100

    assert order.quantity == 5

    assert order.stop_loss == 95

    assert order.target == 110


def test_build_sell_order():

    builder = OrderBuilder()

    order = builder.build(

        DummySignal(

            "SELL",

            100

        )

    )

    assert order.side == "SELL"


def test_none_signal():

    builder = OrderBuilder()

    assert builder.build(None) is None


def test_invalid_direction():

    builder = OrderBuilder()

    with pytest.raises(ValueError):

        builder.build(

            DummySignal(

                "ABC",

                100

            )

        )