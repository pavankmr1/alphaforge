from pathlib import Path

# ==========================================
# SAVE REPORT
# ==========================================
def save_report(
    portfolio,
    strategy_name
):

    output_dir = Path(
        "data/backtest_reports"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    fig = portfolio.plot()

    output_file = (
        output_dir /
        f"{strategy_name}.html"
    )

    fig.write_html(
        str(output_file)
    )

    return output_file