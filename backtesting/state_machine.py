from enum import Enum


class StrategyState(Enum):

    IDLE = "IDLE"

    WAIT_SWEEP = "WAIT_SWEEP"

    WAIT_MSS = "WAIT_MSS"

    WAIT_HTF_FVG = "WAIT_HTF_FVG"

    TRACK_LTF_FVG = "TRACK_LTF_FVG"

    WAIT_RETEST = "WAIT_RETEST"

    READY = "READY"

    TRADE_ACTIVE = "TRADE_ACTIVE"

    COMPLETE = "COMPLETE"