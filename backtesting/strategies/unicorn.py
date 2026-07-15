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

    DEFAULT_CONFIG = {

        # "gap_atr": 0.50,

        "stop_buffer": 0.25,

        "target": "DAY_HIGH",

        "min_volume_ratio": 0.0,

        "require_trend": False,

        "retest_timeout": 20,
        "min_gap_atr":0.50,

        "max_gap_atr":2.0

    }
    @classmethod
    def parameter_space(cls):

        return {

            "min_gap_atr":[
                0.3,
                0.5,
                0.7
            ],

            "max_gap_atr":[
                1.5,
                2.0,
                2.5
            ],

            "stop_buffer":[
                0,
                0.25,
                0.5
            ],

            "target":[
                "DAY_HIGH",
                "PDH",
                "2R"
            ],

            "require_trend":[
                False,
                True
            ]

        }

    def __init__(

        self,

        config=None

    ):

        super().__init__({

            **self.DEFAULT_CONFIG,

            **(config or {})

        })

        self.context = StrategyContext()

        self.context.state = StrategyState.WAIT_SWEEP

        self.fvg_counter = 0

        self.day_high = None

        self.previous_day_high = None
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

    def set_previous_day_high(self, value):

        self.previous_day_high = value

    def quality_bullish_fvg(self, candle):

        gap = candle["BullishFVG_GapATR"]

        return (

            candle["QUALITY_BULLISH_FVG"]

            and

            self.config["min_gap_atr"]

            <= gap

            <=

            self.config["max_gap_atr"]

        )

    def resolve_target(

        self,

        entry_price,

        stop,

        candle=None

    ):

        target_mode = self.config["target"]

        if target_mode == "DAY_HIGH":

            return self.day_high

        if target_mode == "PDH":
            

            if candle is not None and "PreviousDayHigh" in candle.index:

                return candle["PreviousDayHigh"]

            elif self.previous_day_high is None:
                return self.day_high
            return self.previous_day_high

        if target_mode == "2R":

            risk = entry_price - stop

            if risk <= 0:

                return None

            return entry_price + (2 * risk)

        return self.day_high
    def update_5m(self, candle):

        if self.is_state(StrategyState.WAIT_SWEEP):

            if candle["SWEEP_SWING_LOW"]:

                self.context.latest_sweep = candle.name

                self.set_state(
                    StrategyState.WAIT_MSS
                )
                self.log_event(
                    candle,
                    "SWEEP"
                )

                return

        if self.is_state(StrategyState.WAIT_MSS):

            if candle["BOS_BULLISH"]:

                self.context.latest_mss = candle.name

                self.set_state(
                    StrategyState.WAIT_HTF_FVG
                )
                self.log_event(
                    candle,
                    "MSS"
                )

                return

        if self.is_state(StrategyState.WAIT_HTF_FVG):

            if self.quality_bullish_fvg(candle):

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
                self.log_event(
                    candle,
                    "HTF_FVG"
                )
        

    def update_1m(self, candle):

        # Always clean broken FVGs
        self.cleanup_fvgs(candle)

        # Register new 1m FVGs while tracking
        if self.is_state(StrategyState.TRACK_LTF_FVG):

            if self.quality_bullish_fvg(candle):

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
                self.log_event(
                    candle,
                    "LTF_FVG"
                )

        # From now on every candle checks for entry
        if self.is_state(StrategyState.WAIT_RETEST):

            self.try_entry(candle)

    def get_signals(self):

        return self.context.signals
    # ==========================================================
    # POP SIGNAL
    # ==========================================================

    def pop_signal(self):

        """
        Returns the oldest signal and removes it
        from the queue.
        """

        if not self.context.signals:

            return None

        return self.context.signals.pop(0)

    def reset(self):

        self.context = StrategyContext()

        self.context.state = StrategyState.WAIT_SWEEP

        self.fvg_counter = 0

        self.day_high = None

        self.previous_day_high = None

    # ==========================================================
    # RESET STATE
    # ==========================================================

    def reset_state(self):

        """
        Reset ONLY the strategy state after a trade.

        Keeps:
            - Signals
            - Event Log
            - Statistics

        Clears:
            - Current setup
            - Active FVGs
            - Current trade context
        """

        self.set_state(
            StrategyState.WAIT_SWEEP
        )

        self.context.latest_sweep = None

        self.context.latest_mss = None

        if hasattr(self.context, "htf_fvg"):
            self.context.htf_fvg = None

        if hasattr(self.context, "execution_fvg"):
            self.context.execution_fvg = None

        self.context.active_fvgs.clear()

        self.day_high = None

        # self.previous_day_high = None
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

                buffer = self.config["stop_buffer"]

                if candle["Close"] < (fvg.bottom - buffer):
                    self.invalidate_fvg(fvg)
                    self.log_event(
                        candle,
                        "FVG_INVALIDATED",
                        {

                            "top": fvg.top,

                            "bottom": fvg.bottom

                        }

                    )
    
    # ==========================================================
    # RETEST
    # ==========================================================

    def retest(self, candle, fvg):

        buffer = candle["ATR14"] * self.config["stop_buffer"]

        return (

            candle["Low"] <= (fvg.top + buffer)

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
        # ==========================================================
        # TREND FILTER
        # ==========================================================

        if self.config["require_trend"]:

            if not candle["BULLISH_TREND_V2"]:
                return
        fvg = self.latest_valid_fvg()

        if fvg is None:

            return

        if not self.retest(candle, fvg):

            return

        entry_price = candle["Close"]

        buffer = (

            candle["ATR14"]

            *

            self.config["stop_buffer"]

        )

        stop = fvg.bottom - buffer

        target = self.resolve_target(

            entry_price,

            stop,

            candle

        )

        if target is None:

            return

        self.context.execution_fvg = fvg
        self.mark_used(fvg)
        self.log_event(
            candle,
            "ENTRY"
        )

        self.create_signal(

            entry_time=candle.name,

            entry_price=entry_price,

            stop=stop,

            target=target,

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
    # EVENT LOG
    # ==========================================================

    def log_event(

        self,

        candle,

        event,

        details=None

    ):

        self.context.event_log.append(

            {

                "time": candle.name,

                "event": event,

                "details": details

            }

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
from backtesting.strategy_registry import StrategyRegistry

StrategyRegistry.register(
    "UNICORN",
    UnicornStrategy
)