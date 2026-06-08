from experiment_tracker import (
    load_history
)

# ==========================================
# SCORE STRATEGY
# ==========================================
def calculate_score(
    metrics
):

    total_return = (
        metrics.get(
            "total_return",
            0
        )
    )

    sharpe = (
        metrics.get(
            "sharpe_ratio",
            0
        )
    )

    win_rate = (
        metrics.get(
            "win_rate",
            0
        )
    )

    drawdown = abs(
        metrics.get(
            "max_drawdown",
            0
        )
    )

    score = (

        (total_return * 100)

        + (sharpe * 10)

        + (win_rate * 50)

        - (drawdown * 100)
    )

    return round(score, 2)

# ==========================================
# RANK STRATEGIES
# ==========================================
def rank_strategies():

    history = load_history()

    ranked = []

    for experiment in history:

        metrics = experiment["metrics"]

        score = calculate_score(
            metrics
        )

        ranked.append({

            "strategy_name":
            experiment[
                "strategy_name"
            ],

            "score":
            score,

            "metrics":
            metrics
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    ranked = rank_strategies()

    print(
        "\n===== STRATEGY RANKINGS ====="
    )

    for idx, item in enumerate(
        ranked,
        start=1
    ):

        print(
            f"\n#{idx}"
        )

        print(
            f"Strategy: "
            f"{item['strategy_name']}"
        )

        print(
            f"Score: "
            f"{item['score']}"
        )

        print(
            f"Metrics: "
            f"{item['metrics']}"
        )