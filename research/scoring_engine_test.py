import yfinance as yf
import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.scoring_engine import (
    bullish_score
)

# ==================================
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

context = build_context(data)

# ==================================
# SCORE ENGINE
# ==================================

score = bullish_score(
    data,
    context
)

# ==================================
# REPORT
# ==================================

print()
print("=" * 60)
print("ALPHAFORGE SCORING ENGINE")
print("=" * 60)

print()
print("SCORE SUMMARY")
print("-" * 60)

print(
    score.describe()
)

print()

print("SCORE DISTRIBUTION")
print("-" * 60)

print(
    score
    .value_counts()
    .sort_index()
)

print()

print("TOP SCORING CANDLES")
print("-" * 60)

top_scores = pd.DataFrame({

    "Close": data["Close"],

    "Score": score,

    "BullishContext":
        context["BULLISH_CONTEXT"],

    "BullishStructure":
        data["BULLISH_STRUCTURE"],

    "StrongBOS":
        data["STRONG_BOS_BULLISH"],

    "Confirmation":
        data["BULLISH_CONFIRMATION"],

    "Sweep":
        data["SWEEP_SWING_LOW"]

})

top_scores = top_scores.sort_values(
    "Score",
    ascending=False
)

print(
    top_scores.head(20)
)

print()

print("HIGH QUALITY SETUPS")
print("-" * 60)

high_quality = (
    score >= 6
)

print(
    "Score >= 6:",
    int(high_quality.sum())
)

print()

print(
    top_scores[
        top_scores["Score"] >= 6
    ].to_string()
)

print()

print("VERY HIGH QUALITY SETUPS")
print("-" * 60)

very_high_quality = (
    score >= 7
)

print(
    "Score >= 7:",
    int(
        very_high_quality.sum()
    )
)

print()

print(
    top_scores[
        top_scores["Score"] >= 7
    ].to_string()
)

print()

print("ELITE SETUPS")
print("-" * 60)

elite = (
    score >= 8
)

print(
    "Score >= 8:",
    int(elite.sum())
)

print()

print(
    top_scores[
        top_scores["Score"] >= 8
    ].to_string()
)