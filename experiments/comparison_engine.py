from experiment_tracker import (
    load_history
)

# ==========================================
# COMPARE LAST TWO RUNS
# ==========================================
def compare_latest_runs():

    history = load_history()

    if len(history) < 2:

        print(
            "Not enough experiments."
        )

        return

    latest = history[-1]

    previous = history[-2]

    latest_return = (
        latest["metrics"]
        ["total_return"]
    )

    previous_return = (
        previous["metrics"]
        ["total_return"]
    )

    delta = (
        latest_return -
        previous_return
    )

    print("\n===== COMPARISON =====")

    print(
        f"Previous Return: "
        f"{previous_return}"
    )

    print(
        f"Latest Return: "
        f"{latest_return}"
    )

    print(
        f"Delta: {delta}"
    )

    if delta > 0:

        print(
            "Strategy improved."
        )

    else:

        print(
            "Strategy worsened."
        )