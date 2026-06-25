from typing import List, Optional

from backtesting.strategy import Strategy
from backtesting.state_machine import StrategyState
from backtesting.models import (
    FVG,
    TradeSignal,
    StrategyContext
)


class UnicornStrategy(Strategy):

    """
    ICT Unicorn Strategy

    HTF:
        5 Minute

    LTF:
        1 Minute

    Entry:

        Sweep
        ↓
        MSS
        ↓
        HTF FVG
        ↓
        Latest Valid LTF FVG
        ↓
        Retest
        ↓
        Buy

    """

    def __init__(self):

        self.context = StrategyContext()

        self.context.state = StrategyState.WAIT_SWEEP

        self.fvg_counter = 0
        self.day_high = None
    # ==========================================================
    # STATE
    # ==========================================================

    def state(self):

        return self.context.state


    def set_state(self, new_state):

        self.context.state = new_state


    def is_state(self, state):

        return self.context.state == state
    # ==========================================================
    # REQUIRED INTERFACE
    # ==========================================================
    def set_day_high(self, value):

        self.day_high = value
    def update_5m(self, candle):

        if self.is_state(StrategyState.WAIT_SWEEP):

            if candle["SWEEP_SWING_LOW"]:

                self.context.latest_sweep = candle.name

                self.set_state(
                    StrategyState.WAIT_MSS
                )

                return

        if self.is_state(StrategyState.WAIT_MSS):

            if candle["BOS_BULLISH"]:

                self.context.latest_mss = candle.name

                self.set_state(
                    StrategyState.WAIT_HTF_FVG
                )

                return

        if self.is_state(StrategyState.WAIT_HTF_FVG):

            if candle["QUALITY_BULLISH_FVG"]:

                htf_fvg = self.register_fvg(

                    direction="bullish",

                    timeframe="5m",

                    created=candle.name,

                    top=candle["BullishFVG_Top"],

                    bottom=candle["BullishFVG_Bottom"],

                    gap=candle["BullishFVG_Gap"],

                    gap_atr=candle["BullishFVG_GapATR"]

                )

                self.context.htf_fvg = htf_fvg

                self.set_state(

                    StrategyState.TRACK_LTF_FVG

                )

    def update_1m(self, candle):

        # Always clean broken FVGs
        self.cleanup_fvgs(candle)

        # Register new 1m FVGs while tracking
        if self.is_state(StrategyState.TRACK_LTF_FVG):

            if candle["QUALITY_BULLISH_FVG"]:

                self.register_fvg(
                    direction="bullish",
                    timeframe="1m",
                    created=candle.name,
                    top=candle["BullishFVG_Top"],
                    bottom=candle["BullishFVG_Bottom"],
                    gap=candle["BullishFVG_Gap"],
                    gap_atr=candle["BullishFVG_GapATR"]
                )

                self.set_state(
                    StrategyState.WAIT_RETEST
                )

        # From now on every candle checks for entry
        if self.is_state(StrategyState.WAIT_RETEST):

            self.try_entry(candle)

    def get_signals(self):

        return self.context.signals

    def reset(self):

        self.context = StrategyContext()

        self.context.state = StrategyState.WAIT_SWEEP

        self.fvg_counter = 0

        self.day_high = None

    # ==========================================================
    # FVG MANAGEMENT
    # ==========================================================

    def register_fvg(
        self,
        direction,
        timeframe,
        created,
        top,
        bottom,
        gap,
        gap_atr
    ):
        for existing in self.context.active_fvgs:

            if (
                existing.valid
                and existing.direction == direction
                and existing.timeframe == timeframe
                and abs(existing.top - top) < 0.01
                and abs(existing.bottom - bottom) < 0.01
            ):
                return existing
        self.fvg_counter += 1

        fvg = FVG(

            id=self.fvg_counter,

            direction=direction,

            timeframe=timeframe,

            created=created,

            top=top,

            bottom=bottom,

            gap=gap,

            gap_atr=gap_atr

        )

        self.context.active_fvgs.append(
            fvg
        )

        return fvg
    # ==========================================================
    # REPLACE WITH NEWER FVG
    # ==========================================================

    # def register_latest_fvg(self, fvg):

    #     latest = self.latest_valid_fvg()

    #     if latest is None:

    #         self.context.active_fvgs.append(fvg)

    #         return

    #     # ------------------------------------------------------

    #     # Newer FVG formed

    #     # ------------------------------------------------------

    #     if fvg.created > latest.created:

    #         # If latest still valid,
    #         # keep both for now.

    #         self.context.active_fvgs.append(fvg)

    # ==========================================================

    def get_active_fvgs(
        self,
        timeframe=None,
        direction=None
    ):

        fvgs = [

            f

            for f in self.context.active_fvgs

            if f.valid

        ]

        if timeframe:

            fvgs = [

                f

                for f in fvgs

                if f.timeframe == timeframe

            ]

        if direction:

            fvgs = [

                f

                for f in fvgs

                if f.direction == direction

            ]

        return fvgs

    # ==========================================================

    def invalidate_fvg(
        self,
        fvg
    ):

        fvg.valid = False

        fvg.broken = True

    # ==========================================================

    def mark_mitigated(
        self,
        fvg
    ):

        fvg.mitigated = True

    # ==========================================================

    def mark_used(
        self,
        fvg
    ):

        fvg.used = True

    # ==========================================================

    def latest_fvg(
        self,
        timeframe,
        direction
    ):

        fvgs = self.get_active_fvgs(

            timeframe=timeframe,

            direction=direction

        )

        if len(fvgs) == 0:

            return None

        return max(

            fvgs,

            key=lambda x: x.created

        )

    # +=========================================================
    # Summary
    # ==========================================================

    def summary(self):

        print()

        print("=" * 60)

        print("UNICORN ENGINE")

        print("=" * 60)

        print("State :", self.context.state)

        print("Sweep :", self.context.latest_sweep)

        print("MSS   :", self.context.latest_mss)

        print("FVGs  :", len(self.context.active_fvgs))

        print("Signals :", len(self.context.signals))

    # ==========================================================
    # REMOVE BROKEN FVGs
    # ==========================================================

    def cleanup_fvgs(self, candle):

        for fvg in self.context.active_fvgs:

            if not fvg.valid:
                continue
            if fvg.used:
                continue
            if fvg.direction == "bullish":

                buffer = 0.25

                if candle["Close"] < (fvg.bottom - buffer):
                    self.invalidate_fvg(fvg)
    
    # ==========================================================
    # RETEST
    # ==========================================================

    def retest(self, candle, fvg):

        return (

            candle["Low"] <= fvg.top

            and

            candle["Close"] >= fvg.bottom

        )
    # ==========================================================
    # ENTRY
    # ==========================================================

    def try_entry(self, candle):
        if self.is_state(
            StrategyState.TRADE_ACTIVE
        ):
            return
        if self.day_high is None:
            return
        fvg = self.latest_valid_fvg()

        if fvg is None:

            return

        if not self.retest(candle, fvg):

            return
        self.context.execution_fvg = fvg
        self.mark_used(fvg)

        self.create_signal(

            entry_time=candle.name,

            entry_price=candle["Close"],

            stop=fvg.bottom,

            target=self.day_high,

            reason="UNICORN_MTF"

        )

        self.set_state(

            StrategyState.TRADE_ACTIVE

        )
    # ==========================================================
    # LATEST VALID FVG
    # ==========================================================

    def latest_valid_fvg(self):

        fvgs = [

            f

            for f in self.context.active_fvgs

            if f.valid
            and not f.used
            and f.direction == "bullish"
            and f.timeframe == "1m"

        ]

        if not fvgs:

            return None

        return max(

            fvgs,

            key=lambda x: x.created

        )
    # ==========================================================
    # SIGNALS
    # ==========================================================

    def create_signal(

        self,

        entry_time,

        entry_price,

        stop,

        target,

        reason,

        confidence=1.0

    ):

        signal = TradeSignal(

            strategy="UNICORN",

            direction="LONG",

            timeframe="5m->1m",

            entry_time=entry_time,

            entry_price=entry_price,

            stop_loss=stop,

            target=target,

            reason=reason,

            confidence=confidence

        )

        self.context.signals.append(

            signal

        )

        return signal