from paper_trading.order import Order


class OrderBuilder:
    """
    AlphaForge V4

    Converts strategy TradeSignals into executable Orders.

    Strategy
        ↓
    TradeSignal
        ↓
    OrderBuilder
        ↓
    Order
    """

    def build(self, signal):

        if signal is None:

            return None

        direction = signal.direction.upper()

        if direction not in ("BUY", "SELL"):

            raise ValueError(

                f"Unsupported direction: {signal.direction}"

            )

        quantity = getattr(

            signal,

            "quantity",

            1

        )

        return Order(

            side=direction,

            quantity=quantity,

            price=signal.entry_price,

            stop_loss=getattr(

                signal,

                "stop_loss",

                None

            ),

            target=getattr(

                signal,

                "target",

                None

            ),

            timestamp=getattr(

                signal,

                "entry_time",

                None

            )

        )