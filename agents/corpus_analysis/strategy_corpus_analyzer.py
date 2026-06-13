from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies"
)

strategy_type_counter = Counter()
indicator_counter = Counter()
session_counter = Counter()
htf_counter = Counter()
ltf_counter = Counter()
rr_counter = Counter()

total_strategies = 0

for file in STRATEGY_DIR.glob("*.json"):

    total_strategies += 1

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    # -----------------------
    # Strategy Type
    # -----------------------
    strategy_type = strategy.get(
        "strategy_type",
        "UNKNOWN"
    )

    strategy_type_counter[
        strategy_type
    ] += 1

    # -----------------------
    # Indicators
    # -----------------------
    indicators = strategy.get(
        "indicators",
        []
    )

    for indicator in indicators:

        indicator_counter[
            indicator.strip()
        ] += 1

    # -----------------------
    # Sessions
    # -----------------------
    sessions = strategy.get(
        "sessions",
        []
    )

    for session in sessions:

        session_counter[
            session.strip()
        ] += 1

    # -----------------------
    # HTF
    # -----------------------
    htf = strategy.get(
        "htf"
    )

    if htf:

        htf_counter[
            str(htf)
        ] += 1

    # -----------------------
    # LTF
    # -----------------------
    ltf = strategy.get(
        "ltf"
    )

    if ltf:

        ltf_counter[
            str(ltf)
        ] += 1

    # -----------------------
    # Risk Reward
    # -----------------------
    rr = strategy.get(
        "risk_reward"
    )

    if rr:

        rr_counter[
            str(rr)
        ] += 1

print(
    f"\nStrategies Scanned: "
    f"{total_strategies}"
)

print(
    "\n===== TOP STRATEGY TYPES ====="
)
print(
    strategy_type_counter.most_common(15)
)

print(
    "\n===== TOP INDICATORS ====="
)
print(
    indicator_counter.most_common(25)
)

print(
    "\n===== TOP SESSIONS ====="
)
print(
    session_counter.most_common(15)
)

print(
    "\n===== HTF ====="
)
print(
    htf_counter.most_common(15)
)

print(
    "\n===== LTF ====="
)
print(
    ltf_counter.most_common(15)
)

print(
    "\n===== RISK REWARD ====="
)
print(
    rr_counter.most_common(15)
)