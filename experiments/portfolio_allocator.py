from experiment_tracker import (
    load_history
)

# ==========================================
# BUILD SIMPLE PORTFOLIO
# ==========================================
def build_portfolio():

    history = load_history()

    if len(history) == 0:

        raise ValueError(
            "No experiments found."
        )

    portfolio = []

    for experiment in history:

        metrics = experiment["metrics"]

        portfolio.append({

            "strategy_name":
            experiment[
                "strategy_name"
            ],

            "expected_return":
            metrics[
                "total_return"
            ],

            "sharpe_ratio":
            metrics[
                "sharpe_ratio"
            ],

            "max_drawdown":
            metrics[
                "max_drawdown"
            ]
        })

    return portfolio

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    portfolio = build_portfolio()

    print(
        "\n===== PORTFOLIO ====="
    )

    for strategy in portfolio:

        print("\n----------------")

        for key, value in (
            strategy.items()
        ):

            print(
                f"{key}: {value}"
            )