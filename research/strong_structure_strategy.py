import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.state_engine import (
    sequence_signal
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

trend = (
    data["BULLISH_TREND_V2"]
)

sweep = (
    data["BULLISH_SWEEP_REJECTION"]
)

bos = (
    data["STRONG_BOS_BULLISH"]
)

entries = sequence_signal(
    trend,
    sweep,
    bos,
    lookahead=10
)

entries = (
    entries
    .fillna(False)
    .astype(bool)
)

exits = (
    data["STRONG_BOS_BEARISH"]
)

exits = (
    exits
    .shift(1)
    .fillna(False)
    .astype(bool)
)

portfolio = vbt.Portfolio.from_signals(
    close=data["Close"].astype(float),
    entries=entries,
    exits=exits,
    init_cash=100000,
    freq="1D"
)

print()
print("=" * 60)
print("STRONG STRUCTURE STRATEGY")
print("=" * 60)

print("Signals:", int(entries.sum()))
print("Trades:", portfolio.trades.count())
print("Return:", round(float(portfolio.total_return()), 4))
print("Sharpe:", round(float(portfolio.sharpe_ratio()), 4))
print("Win Rate:", round(float(portfolio.trades.win_rate()), 4))
print("Max DD:", round(float(portfolio.max_drawdown()), 4))