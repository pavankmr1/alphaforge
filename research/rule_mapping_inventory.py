from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

counter = Counter()

for file in STRATEGY_DIR.glob(
    "*.json"
):

    try:

        strategy = json.loads(
            file.read_text()
        )

        compiled = strategy.get(
            "compiled_entry_logic",
            []
        )

        for item in compiled:

            mappings = item.get(
                "compiled_logic",
                []
            )

            for mapping in mappings:

                logic_type = mapping.get(
                    "logic_type"
                )

                if logic_type:

                    counter[
                        logic_type
                    ] += 1

    except Exception:
        pass

print()
print("=" * 50)
print("RULE MAPPING INVENTORY")
print("=" * 50)

for logic_type, count in counter.most_common():

    print(
        f"{logic_type}: {count}"
    )