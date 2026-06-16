from pathlib import Path
import json

STRATEGY_DIR = Path(
    "data/compiled_strategies_v2"
)

ready = 0
needs_smc = 0
needs_fib = 0
needs_sessions = 0
broken = 0

SMC_FIELDS = {
    "FVG",
    "DemandZone",
    "SupplyZone",
    "POI",
    "OrderBlock",
    "OrderBlockPOI",
    "LiquidityHigh",
    "LiquidityLow",
    "BOS"
}

FIB_FIELDS = {
    "Fib0.382",
    "Fib0.60",
    "Fib0.705",
    "FibonacciPivot",
    "FibonacciRetracement50_618Zone"
}

SESSION_FIELDS = {
    "LondonSessionOpen",
    "London_Open",
    "New_York_Open"
}

for file in STRATEGY_DIR.glob("*.json"):

    strategy = json.loads(
        file.read_text()
    )

    text = json.dumps(strategy)

    if any(
        x in text
        for x in SMC_FIELDS
    ):
        needs_smc += 1

    elif any(
        x in text
        for x in FIB_FIELDS
    ):
        needs_fib += 1

    elif any(
        x in text
        for x in SESSION_FIELDS
    ):
        needs_sessions += 1

    else:
        ready += 1

print()
print("=" * 40)
print("ALPHAFORGE READINESS REPORT")
print("=" * 40)

print(f"Ready: {ready}")
print(f"Needs SMC: {needs_smc}")
print(f"Needs Fibonacci: {needs_fib}")
print(f"Needs Sessions: {needs_sessions}")
print(f"Total: {ready + needs_smc + needs_fib + needs_sessions}")