from collections import Counter
from pathlib import Path
import json

ALIASES = {

    # Trend
    "Bullish": "GREEN_CANDLE",
    "Bearish": "RED_CANDLE",

    # Consecutive candles
    "ConsecutiveGreenCandles": "CONSEC_GREEN_3",

    # Confirmation
    "ConfirmationCandle": "BULLISH_CONFIRMATION",
    "ConfirmationCandles": "BULLISH_CONFIRMATION",
    "Confirmation/Rejection": "LONG_LOWER_WICK",

    # Momentum
    "Momentum": "BULLISH_CONFIRMATION",
    "BuyerDominance": "BULLISH_CONFIRMATION",
    "SellerDominant": "BEARISH_CONFIRMATION",

    # Wick logic
    "WickZone": "LONG_LOWER_WICK",

    # Structure aliases
    "PrevLow": "PreviousLow",
    "PrevCandleHigh": "PreviousHigh",
    "PriceLow": "Low",
    "Price High": "High",

    # Session aliases
    "SessionHigh": "PreviousDayHigh",
    "PriorSessionHigh": "PreviousDayHigh",
    "PriorSessionLow": "PreviousDayLow",

    # Breakout aliases
    "BreakoutCandleHigh": "PreviousHigh"
}

counter = Counter()

strategy_dir = Path(
    "data/compiled_strategies_v3"
)

for file in strategy_dir.glob("*.json"):

    try:
        strategy = json.loads(
            file.read_text()
        )
    except:
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

                if operand in ALIASES:

                    counter[
                        operand
                    ] += 1

print()
print("=" * 60)
print("ALIAS OPPORTUNITIES")
print("=" * 60)

for k, v in counter.most_common():

    print(
        f"{k:30} -> {ALIASES[k]:25} ({v})"
    )