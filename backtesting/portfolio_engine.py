import vectorbt as vbt

from loguru import logger

# ==========================================
# RUN PORTFOLIO
# ==========================================
def run_backtest(
    close,
    entries,
    exits
):

    logger.info(
        "Running vectorbt portfolio..."
    )

    portfolio = vbt.Portfolio.from_signals(
        close,
        entries,
        exits,
        init_cash=100000,
        freq="1min"
    )

    return portfolio