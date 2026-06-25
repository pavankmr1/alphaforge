import yfinance as yf

data = yf.download(
    "^NSEI",
    period="7d",
    interval="1m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

print()
print("=" * 80)
print("EOD EXIT TEST")
print("=" * 80)

count = 0

for ts in data.index:

    ist_time = ts.tz_convert(
        "Asia/Kolkata"
    )

    eod_exit = (

        ist_time.hour == 15

        and

        ist_time.minute == 15

    )

    if eod_exit:

        count += 1

        print(
            f"EOD Candle #{count}:",
            ist_time
        )

print()
print(
    "Total EOD Candles:",
    count
)