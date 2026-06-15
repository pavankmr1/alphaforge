from pathlib import Path
from collections import Counter
import json

COMPILED_DIR = Path(
    "data/compiled_strategies_v2"
)

invalid_counter = Counter()

for file in COMPILED_DIR.glob("*.json"):

    strategy = json.loads(
        file.read_text()
    )

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

            left = str(
                rule.get("left")
            )

            right = str(
                rule.get("right")
            )

            if left not in [
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
                "Pivot",
                "None"
            ]:

                invalid_counter[left] += 1

            if right not in [
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
                "Pivot",
                "None"
            ]:

                invalid_counter[right] += 1

print("\nTOP REMAINING GAPS\n")

for k, v in invalid_counter.most_common(50):

    print(
        f"{k}: {v}"
    )