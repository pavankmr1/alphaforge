from pathlib import Path
import json
from collections import Counter

STRATEGY_DIR = Path(
    "data/compiled_strategies"
)

OUTPUT_FILE = Path(
    "data/concept_inventory.json"
)

CONCEPT_ALIASES = {

    "fvg": [
        "fvg",
        "fair value gap"
    ],

    "bos": [
        "bos",
        "break of structure"
    ],

    "choch": [
        "choch",
        "change of character"
    ],

    "mss": [
        "mss",
        "market structure shift"
    ],

    "order block": [
        "order block",
        "ob"
    ],

    "liquidity sweep": [
        "liquidity sweep",
        "liquidity grab",
        "stop hunt",
        "idm"
    ],

    "ote": [
        "ote",
        "optimal trade entry"
    ],

    "breaker block": [
        "breaker block"
    ],

    "mitigation": [
        "mitigation"
    ],

    "displacement": [
        "displacement"
    ],

    "vwap": [
        "vwap"
    ]
}

counter = Counter()
strategy_count = 0

for file in STRATEGY_DIR.glob("*.json"):
    strategy_count += 1

print(f"Strategies scanned: {strategy_count}")
for file in STRATEGY_DIR.glob("*.json"):
    
    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    text_blob = " ".join(

        strategy.get(
            "entry_conditions",
            []
        )

        +

        strategy.get(
            "exit_conditions",
            []
        )

        +

        strategy.get(
            "indicators",
            []
        )

        +

        [
            strategy.get(
                "notes",
                ""
            )
        ]
    ).lower()

    for concept, aliases in CONCEPT_ALIASES.items():

        for alias in aliases:

            if alias in text_blob:

                counter[concept] += 1
                break

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        dict(counter),
        f,
        indent=4
    )

print(
    json.dumps(
        dict(counter),
        indent=4
    )
)