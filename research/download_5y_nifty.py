from dhanhq import DhanContext, dhanhq
from dotenv import load_dotenv

import pandas as pd
import os

from datetime import datetime
from datetime import timedelta

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

DHAN_CLIENT_ID = os.getenv(
    "DHAN_CLIENT_ID"
)

DHAN_ACCESS_TOKEN = os.getenv(
    "DHAN_ACCESS_TOKEN"
)

# ==========================================
# DHAN
# ==========================================

context = DhanContext(
    client_id=DHAN_CLIENT_ID,
    access_token=DHAN_ACCESS_TOKEN
)

dhan = dhanhq(context)

# ==========================================
# CONFIG
# ==========================================

SECURITY_ID = "13"  # NIFTY 50

START_DATE = "2021-01-01"
END_DATE = datetime.now().strftime(
    "%Y-%m-%d"
)

CHUNK_DAYS = 89

# ==========================================
# DOWNLOAD
# ==========================================

start = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
)

end = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
)

all_chunks = []

downloaded_rows = 0

while start < end:

    chunk_end = min(
        start + timedelta(days=CHUNK_DAYS),
        end
    )

    from_date = start.strftime(
        "%Y-%m-%d"
    )

    to_date = chunk_end.strftime(
        "%Y-%m-%d"
    )

    print()
    print("=" * 70)
    print(
        f"DOWNLOADING {from_date} -> {to_date}"
    )
    print("=" * 70)

    response = dhan.intraday_minute_data(
        security_id=SECURITY_ID,
        exchange_segment="IDX_I",
        instrument_type="INDEX",
        from_date=from_date,
        to_date=to_date
    )

    if response["status"] != "success":

        print(
            "FAILED:",
            response["remarks"]
        )

        start = chunk_end + timedelta(days=1)
        continue

    data = response["data"]

    df = pd.DataFrame({

        "timestamp":
            data["timestamp"],

        "open":
            data["open"],

        "high":
            data["high"],

        "low":
            data["low"],

        "close":
            data["close"],

        "volume":
            data["volume"]

    })

    downloaded_rows += len(df)

    print(
        f"Rows: {len(df):,}"
    )

    all_chunks.append(df)

    start = chunk_end + timedelta(days=1)

# ==========================================
# MERGE
# ==========================================

print()
print("=" * 70)
print("MERGING DATA")
print("=" * 70)

master_df = pd.concat(
    all_chunks,
    ignore_index=True
)

master_df.drop_duplicates(
    subset=["timestamp"],
    inplace=True
)

master_df.sort_values(
    "timestamp",
    inplace=True
)

master_df["datetime"] = pd.to_datetime(
    master_df["timestamp"],
    unit="s"
)

# ==========================================
# SAVE
# ==========================================

os.makedirs(
    "data/raw",
    exist_ok=True
)

output_file = (
    "data/raw/nifty_1m_5y_master.csv"
)

master_df.to_csv(
    output_file,
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print()
print("=" * 70)
print("DOWNLOAD COMPLETE")
print("=" * 70)

print(
    "Rows:",
    f"{len(master_df):,}"
)

print(
    "Start:",
    master_df["datetime"].min()
)

print(
    "End:",
    master_df["datetime"].max()
)

print(
    "Saved:",
    output_file
)