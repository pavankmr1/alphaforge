from pathlib import Path
import json

STRATEGY_FILE = Path(
    "data/compiled_strategies_v3/GAUTAM JHA TRADING STRATEGY.json"
)

strategy = json.loads(
    STRATEGY_FILE.read_text()
)

print()
print("=" * 70)
print("TOP STRATEGY DEEP DIVE")
print("=" * 70)

print()
print("NAME:")
print(strategy["name"])

print()
print("TYPE:")
print(strategy["strategy_type"])

print()
print("INDICATORS:")
for x in strategy.get(
    "indicators",
    []
):
    print("-", x)

print()
print("ENTRY CONDITIONS:")
for x in strategy.get(
    "entry_conditions",
    []
):
    print("-", x)

print()
print("EXIT CONDITIONS:")
for x in strategy.get(
    "exit_conditions",
    []
):
    print("-", x)

print()
print("COMPILED LOGIC:")
for item in strategy.get(
    "compiled_entry_logic",
    []
):
    print()
    print(
        item.get(
            "original_condition"
        )
    )

    if "dsl" in item:
        print(
            item["dsl"]
        )

    if "compiled_logic" in item:
        print(
            item["compiled_logic"]
        )