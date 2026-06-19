from pathlib import Path
import json

from backtesting.feature_engine import compute_features
import yfinance as yf

# ==========================================
# LOAD SAMPLE DATA
# ==========================================

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

available_features = set(
    data.columns
)

# ==========================================
# SCAN CORPUS
# ==========================================

strategy_dir = Path(
    "data/compiled_strategies_v3"
)

supported = set()
unsupported = set()

for file in strategy_dir.glob("*.json"):

    try:

        strategy = json.loads(
            file.read_text()
        )

    except Exception:
        continue

    compiled_logic = strategy.get(
        "compiled_entry_logic",
        []
    )

    for item in compiled_logic:

        dsl = item.get("dsl")

        if not dsl:
            continue

        for rule in dsl.get(
            "rules",
            []
        ):

            for operand in [
                rule.get("left"),
                rule.get("right")
            ]:

                if not operand:
                    continue

                if operand in available_features:

                    supported.add(
                        operand
                    )

                else:

                    unsupported.add(
                        operand
                    )

print()
print("=" * 60)
print("SUPPORTED FEATURES")
print("=" * 60)

for x in sorted(supported):

    print(x)

print()
print("=" * 60)
print("UNSUPPORTED FEATURES")
print("=" * 60)

for x in sorted(unsupported):

    print(x)

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(
    "Supported:",
    len(supported)
)

print(
    "Unsupported:",
    len(unsupported)
)

coverage = (
    len(supported)
    /
    (
        len(supported)
        +
        len(unsupported)
    )
) * 100

print(
    f"Coverage: {coverage:.2f}%"
)