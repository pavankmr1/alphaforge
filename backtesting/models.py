from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ============================================================
# FAIR VALUE GAP
# ============================================================

@dataclass
class FVG:

    id: int

    direction: str

    timeframe: str

    created: datetime

    top: float

    bottom: float

    gap: float

    gap_atr: float

    valid: bool = True

    mitigated: bool = False

    broken: bool = False

    used: bool = False


# ============================================================
# LIQUIDITY SWEEP
# ============================================================

@dataclass
class LiquiditySweep:

    time: datetime

    direction: str

    price: float


# ============================================================
# MARKET STRUCTURE SHIFT
# ============================================================

@dataclass
class MarketStructureShift:

    time: datetime

    direction: str

    price: float


# ============================================================
# TRADE SIGNAL
# ============================================================

@dataclass
class TradeSignal:

    strategy: str

    direction: str

    timeframe: str

    entry_time: datetime

    entry_price: float

    stop_loss: float

    target: float

    reason: str

    confidence: float = 1.0

    metadata: dict = field(default_factory=dict)


# ============================================================
# LIVE TRADE
# ============================================================

@dataclass
class Trade:

    signal: TradeSignal

    status: str = "OPEN"

    exit_time: Optional[datetime] = None

    exit_price: Optional[float] = None

    pnl: float = 0.0

    rr: float = 0.0


# ============================================================
# STRATEGY CONTEXT
# ============================================================

@dataclass
class StrategyContext:

    state: str = "IDLE"

    active_fvgs: list = field(default_factory=list)

    latest_sweep: Optional[LiquiditySweep] = None

    latest_mss: Optional[MarketStructureShift] = None

    active_trade: Optional[Trade] = None

    signals: list = field(default_factory=list)