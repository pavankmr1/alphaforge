from pathlib import Path
from collections import Counter
import json

SUPPORTED = {

    "EMA9",
    "EMA20",
    "EMA50",
    "EMA200",

    "VWAP",

    "RSI14",

    "ATR14",

    "VOL_MA20",

    "Close",
    "Open",
    "High",
    "Low",
    "Volume"
}

counter = Counter()

for file in Path(
    "data/compiled_strategies_v2"
).glob("*.json"):

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

        dsl = item.get("dsl")

        if not dsl:
            continue

        for rule in dsl.get(
            "rules",
            []
        ):

            left = rule.get(
                "left"
            )

            right = rule.get(
                "right"
            )

            for field in [
                left,
                right
            ]:

                if (
                    field
                    and
                    field not in SUPPORTED
                ):

                    counter[field] += 1

print()

for k, v in counter.most_common():

    print(
        f"{k}: {v}"
    )