import pandas as pd

# ==========================================
# LOAD LEADERBOARD
# ==========================================

df = pd.read_csv(
    "data/batch_results/leaderboard.csv"
)

# ==========================================
# CLEAN
# ==========================================

numeric_cols = [
    "total_return",
    "sharpe_ratio",
    "win_rate",
    "max_drawdown"
]

for col in numeric_cols:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)

# ==========================================
# SCORE
# ==========================================

df["score"] = (

    (df["sharpe_ratio"] * 40)

    +

    (df["win_rate"] * 30)

    +

    (df["total_return"] * 20)

    -

    (abs(df["max_drawdown"]) * 10)

)

# ==========================================
# RANK
# ==========================================

df = df.sort_values(
    by="score",
    ascending=False
)

df["rank"] = range(
    1,
    len(df) + 1
)

# ==========================================
# OUTPUT
# ==========================================

cols = [
    "rank",
    "strategy",
    "score",
    "sharpe_ratio",
    "total_return",
    "win_rate",
    "max_drawdown",
    "signals",
    "trades"
]

print()
print("=" * 100)
print("ALPHAFORGE STRATEGY SCORECARD")
print("=" * 100)

print(
    df[cols]
    .head(20)
    .round(4)
    .to_string(index=False)
)

# ==========================================
# SAVE
# ==========================================

output_file = (
    "data/batch_results/"
    "strategy_scorecard.csv"
)

df.to_csv(
    output_file,
    index=False
)

print()
print(
    f"Saved: {output_file}"
)