from pathlib import Path
from collections import Counter
import json

COMPILED_DIR = Path(
    "data/compiled_strategies_v2"
)

VALID_FIELDS = {

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "EMA5",
    "EMA9",
    "EMA10",
    "EMA15",
    "EMA20",
    "EMA21",
    "EMA50",
    "EMA200",

    "VWAP",
    "ATR14",
    "RSI14",

    "VOL_MA20",

    "Support",
    "Resistance",

    "PreviousHigh",
    "PreviousLow",

    "PreviousDayHigh",
    "PreviousDayLow",

    "Pivot"
}

counter = Counter()

for file in COMPILED_DIR.glob("*.json"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    for item in strategy.get(
        "compiled_entry_logic",
        []
    ):

        dsl = item.get(
            "dsl",
            {}
        )

        for rule in dsl.get(
            "rules",
            []
        ):

            left = rule.get("left")
            right = rule.get("right")

            if (
                isinstance(left, str)
                and
                left not in VALID_FIELDS
            ):
                counter[left] += 1

            if (
                isinstance(right, str)
                and
                right not in VALID_FIELDS
            ):
                counter[right] += 1

print()

print("=" * 50)
print("TOP INVALID DSL FIELDS")
print("=" * 50)

for field, count in counter.most_common(100):

    print(
        f"{field}: {count}"
    )

print()
print(
    f"Unique Invalid Fields: {len(counter)}"
)