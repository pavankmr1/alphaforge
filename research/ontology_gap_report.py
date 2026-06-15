from pathlib import Path
import json
from collections import Counter

compiled_dir = Path(
    "data/compiled_strategies_v2"
)

alias_candidates = Counter()
feature_candidates = Counter()
unsupported_candidates = Counter()

ALIAS_FIELDS = {
    "Price",
    "Market",
    "Trend",
    "EMA",
    "AverageVolume",
    "SupportZone",
    "ResistanceZone"
}

UNSUPPORTED_FIELDS = {
    "OrderBlock",
    "Liquidity",
    "CHoCH",
    "BOS",
    "Trendline",
    "MarketProfile"
}

for file in compiled_dir.glob("*.json"):

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

            for field in [left, right]:

                if field in ALIAS_FIELDS:

                    alias_candidates[field] += 1

                elif field in UNSUPPORTED_FIELDS:

                    unsupported_candidates[field] += 1

                else:

                    feature_candidates[field] += 1


print("\nALIASES")
print("=" * 40)

for k, v in alias_candidates.most_common():

    print(k, v)

print("\nFEATURES")
print("=" * 40)

for k, v in feature_candidates.most_common(30):

    print(k, v)

print("\nUNSUPPORTED")
print("=" * 40)

for k, v in unsupported_candidates.most_common():

    print(k, v)