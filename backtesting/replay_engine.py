import pandas as pd

from backtesting.trade_manager import TradeManager


class ReplayEngine:

    """
    Generic replay engine.

    Replays any strategy over historical data.

    Responsibilities

        - Feed HTF candles

        - Feed LTF candles

        - Open trades

        - Monitor trades

        - Reset strategy after exit

    """

    def __init__(

        self,

        strategy,

        trade_manager=None

    ):

        self.strategy = strategy

        self.trade_manager = (

            trade_manager

            if trade_manager

            else TradeManager()

        )

    # ==========================================================
    # RUN
    # ==========================================================

    def run(

        self,

        df_5m,

        df_1m

    ):

        print()

        print("=" * 80)

        print("REPLAY ENGINE")

        print("=" * 80)

        previous_signal_count = 0

        for ts5, candle5 in df_5m.iterrows():

            # ----------------------------------------
            # Day High
            # ----------------------------------------

            day = ts5.date()

            day_high = df_5m.loc[
                df_5m.index.date == day,
                "High"
            ].max()

            self.strategy.set_day_high(

                day_high

            )

            # ----------------------------------------
            # Update HTF
            # ----------------------------------------

            self.strategy.update_5m(

                candle5

            )

            # ----------------------------------------
            # Get corresponding 1m candles
            # ----------------------------------------

            start = ts5

            end = ts5 + pd.Timedelta(

                minutes=5

            )

            candles_1m = df_1m.loc[
                start:end
            ]

            # ----------------------------------------
            # Feed 1m candles
            # ----------------------------------------

            for ts1, candle1 in candles_1m.iterrows():

                # --------------------
                # Strategy
                # --------------------

                self.strategy.update_1m(

                    candle1

                )

                # --------------------
                # New signal?
                # --------------------

                signal = self.strategy.pop_signal()

                if signal:

                    self.trade_manager.open_trade(signal)

                # --------------------
                # Update trade
                # --------------------

                result = self.trade_manager.update(

                    candle1

                )

                # --------------------
                # Trade finished
                # --------------------

                if result is not None:

                    print(

                        f"{ts1} | {result}"

                    )

                    self.strategy.reset_state()

        print()

        print("=" * 80)

        print("REPLAY COMPLETE")

        print("=" * 80)
