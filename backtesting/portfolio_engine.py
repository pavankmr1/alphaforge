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

    close = close.astype(float)

    entries = (
        entries
        .fillna(False)
        .astype(bool)
    )

    exits = (
        exits
        .fillna(False)
        .astype(bool)
    )

    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entries,
        exits=exits,
        init_cash=100000,
        freq="1D"
    )

    return portfolio