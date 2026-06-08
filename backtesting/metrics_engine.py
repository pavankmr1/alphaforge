def calculate_metrics(
    portfolio
):

    return {

        "total_return":
        float(
            portfolio.total_return()
        ),

        "total_profit":
        float(
            portfolio.total_profit()
        ),

        "max_drawdown":
        float(
            portfolio.max_drawdown()
        ),

        "sharpe_ratio":
        float(
            portfolio.sharpe_ratio()
        ),

        "win_rate":
        float(
            portfolio.trades.win_rate()
        )
    }