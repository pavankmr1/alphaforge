import vectorbt as vbt
import yfinance as yf

from loguru import logger

# ==========================================
# DOWNLOAD DATA
# ==========================================
logger.info(
    "Downloading market data..."
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

close = data["Close"].squeeze()

# ==========================================
# SIMPLE SIGNALS
# ==========================================
fast_ma = close.rolling(20).mean()

slow_ma = close.rolling(50).mean()

entries = fast_ma > slow_ma

exits = fast_ma < slow_ma

# ==========================================
# PORTFOLIO
# ==========================================
portfolio = vbt.Portfolio.from_signals(
    close,
    entries,
    exits,
    init_cash=100000,
    freq="1D"
)

# ==========================================
# RESULTS
# ==========================================
print("Total Return:", portfolio.total_return())

print("Total Profit:", portfolio.total_profit())

print("Max Drawdown:", portfolio.max_drawdown())

print("Sharpe Ratio:", portfolio.sharpe_ratio())

print("Win Rate:", portfolio.trades.win_rate())

# ==========================================
# SAVE CHART
# ==========================================

fig = portfolio.plot()

fig.write_html(
    "data/backtest_reports/simple_backtest.html"
)