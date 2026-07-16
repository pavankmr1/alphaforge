from paper_trading.models import Position


class PositionManager:
    """
    AlphaForge V4

    Responsible ONLY for managing
    the current trading position.
    """

    def __init__(self):

        self.position = None

    # ==========================================================
    # STATUS
    # ==========================================================

    def has_position(self):

        return self.position is not None

    def current(self):

        return self.position

    # ==========================================================
    # OPEN
    # ==========================================================

    def open_position(

        self,

        direction,

        entry_price,

        quantity,

        entry_time=None

    ):

        if self.has_position():

            raise ValueError(

                "Position already exists."

            )

        self.position = Position(

            direction=direction,

            entry_price=float(entry_price),

            quantity=int(quantity),

            entry_time=entry_time,

            current_price=float(entry_price),

            highest_price=float(entry_price),

            lowest_price=float(entry_price)

        )

        return self.position

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_price(

        self,

        price

    ):

        if not self.has_position():

            return

        self.position.current_price = float(price)

        self.position.highest_price = max(

            self.position.highest_price,

            price

        )

        self.position.lowest_price = min(

            self.position.lowest_price,

            price

        )

    # ==========================================================
    # CLOSE
    # ==========================================================

    def close_position(

        self,

        exit_price,

        exit_time=None

    ):
        if not self.has_position():

            raise ValueError(

                "No open position."

            )

        pnl = (

            exit_price

            - self.position.entry_price

        ) * self.position.quantity

        self.position.realized_pnl = pnl

        closed = self.position

        self.position = None
        closed.exit_price = float(exit_price)

        closed.exit_time = exit_time    

        return closed

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self):

        self.position = None