import yfinance as yf

print()
print("=" * 60)
print("DOWNLOADING DATA")
print("=" * 60)

data_15m = yf.download(
    "^NSEI",
    period="7d",
    interval="15m"
)

data_5m = yf.download(
    "^NSEI",
    period="7d",
    interval="5m"
)

data_1m = yf.download(
    "^NSEI",
    period="7d",
    interval="1m"
)

# flatten columns

for df in [
    data_15m,
    data_5m,
    data_1m
]:
    df.columns = (
        df.columns
        .get_level_values(0)
    )

print()
print("=" * 60)
print("15 MIN")
print("=" * 60)

print(
    "Rows:",
    len(data_15m)
)

print(
    "Start:",
    data_15m.index.min()
)

print(
    "End:",
    data_15m.index.max()
)

print()
print("=" * 60)
print("5 MIN")
print("=" * 60)

print(
    "Rows:",
    len(data_5m)
)

print(
    "Start:",
    data_5m.index.min()
)

print(
    "End:",
    data_5m.index.max()
)

print()
print("=" * 60)
print("1 MIN")
print("=" * 60)

print(
    "Rows:",
    len(data_1m)
)

print(
    "Start:",
    data_1m.index.min()
)

print(
    "End:",
    data_1m.index.max()
)

print()

print("=" * 60)
print("ALIGNMENT CHECK")
print("=" * 60)

print()

print(
    "15m first:",
    data_15m.index[0]
)

print(
    "5m first:",
    data_5m.index[0]
)

print(
    "1m first:",
    data_1m.index[0]
)

print()

print(
    "15m last:",
    data_15m.index[-1]
)

print(
    "5m last:",
    data_5m.index[-1]
)

print(
    "1m last:",
    data_1m.index[-1]
)