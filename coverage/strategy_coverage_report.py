from pathlib import Path
import json

STRATEGY_DIR = Path(
    "data/compiled_strategies"
)

SUPPORTED_FEATURES = {

    "ema",
    "9 ema",
    "20 ema",
    "50 ema",
    "200 ema",

    "vwap",

    "rsi",

    "atr",

    "volume",

    "support and resistance",

    "support/resistance",

    "trendlines",

    "price action"
}

supported = 0
partial = 0
unsupported = 0

results = []

for file in STRATEGY_DIR.glob("*.json"):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    indicators = [

        x.lower()
        for x in strategy.get(
            "indicators",
            []
        )
    ]

    if len(indicators) == 0:

        continue

    matched = 0

    for indicator in indicators:

        for feature in SUPPORTED_FEATURES:

            if feature in indicator:

                matched += 1
                break

    coverage_ratio = (
        matched /
        len(indicators)
    )

    if coverage_ratio >= 0.8:

        status = "SUPPORTED"
        supported += 1

    elif coverage_ratio > 0:

        status = "PARTIAL"
        partial += 1

    else:

        status = "UNSUPPORTED"
        unsupported += 1

    results.append({

        "strategy":
        strategy["name"],

        "status":
        status,

        "coverage":
        round(
            coverage_ratio * 100,
            2
        )
    })

print(
    "\n===== COVERAGE REPORT ====="
)

for item in results:

    print(
        f"{item['strategy']} | "
        f"{item['status']} | "
        f"{item['coverage']}%"
    )

total = (
    supported +
    partial +
    unsupported
)

print("\n===== SUMMARY =====")

print(
    f"Supported: {supported}"
)

print(
    f"Partial: {partial}"
)

print(
    f"Unsupported: {unsupported}"
)

print(
    f"Coverage: "
    f"{round((supported/total)*100,2)}%"
)