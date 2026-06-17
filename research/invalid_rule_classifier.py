from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

categories = Counter()

for file in STRATEGY_DIR.glob(
    "*.json"
):

    try:

        strategy = json.loads(
            file.read_text()
        )

        for item in strategy.get(
            "compiled_entry_logic",
            []
        ):

            dsl = item.get(
                "dsl"
            )

            if not dsl:
                continue

            for rule in dsl.get(
                "rules",
                []
            ):

                if (
                    rule.get(
                        "validation_status"
                    )
                    !=
                    "invalid"
                ):
                    continue

                text = str(rule)

                # =====================
                # TIME
                # =====================
                if any(
                    x in text
                    for x in [
                        "06:00",
                        "10:30",
                        "13:30",
                        "16:30",
                        "17:30",
                        "22:00"
                    ]
                ):

                    categories[
                        "TIME"
                    ] += 1

                # =====================
                # PRICE PATTERN
                # =====================
                elif any(
                    x in text
                    for x in [
                        "High[1]",
                        "Candle3.Low",
                        "Next Candle High",
                        "Midpoint",
                        "5-minute candle",
                        "Confirmation Candle"
                    ]
                ):

                    categories[
                        "PRICE_PATTERN"
                    ] += 1

                # =====================
                # SESSION
                # =====================
                elif any(
                    x in text
                    for x in [
                        "NASDAQ",
                        "US30",
                        "XAUUSD"
                    ]
                ):

                    categories[
                        "SESSION_OR_ASSET"
                    ] += 1

                # =====================
                # EVERYTHING ELSE
                # =====================
                else:

                    categories[
                        "GARBAGE_OR_UNKNOWN"
                    ] += 1

    except Exception:
        pass

print()
print("=" * 60)
print("INVALID RULE CLASSIFICATION")
print("=" * 60)

for name, count in categories.most_common():

    print(
        f"{name}: {count}"
    )