from pydantic import BaseModel
from typing import List, Optional


class StrategySchema(BaseModel):

    name: str

    strategy_type: str

    htf: Optional[str]
    ltf: Optional[str]

    indicators: List[str]

    entry_conditions: List[str]

    exit_conditions: List[str]

    stoploss_logic: str

    target_logic: str

    sessions: List[str]

    risk_reward: Optional[float]

    notes: Optional[str]
    strategy_id: str
    source: str
    source_channel: Optional[str]
    version: str
    created_at: str