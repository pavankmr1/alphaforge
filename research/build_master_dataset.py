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

START_DATE = "2025-01-01"
END_DATE = "2026-06-24"

SECURITY_ID = "13"

# ==========================================
# WINDOWS
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

while start < end:

    chunk_end = min(
        start + timedelta(days=89),
        end
    )

    from_date = start.strftime(
        "%Y-%m-%d"
    )

    to_date = chunk_end.strftime(
        "%Y-%m-%d"
    )

    print()
    print("=" * 60)
    print(
        f"DOWNLOADING {from_date} -> {to_date}"
    )
    print("=" * 60)

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

        "open":
            data["open"],

        "high":
            data["high"],

        "low":
            data["low"],

        "close":
            data["close"],

        "volume":
            data["volume"],

        "timestamp":
            data["timestamp"]

    })

    print(
        "Rows:",
        len(df)
    )

    all_chunks.append(df)

    start = chunk_end + timedelta(days=1)

# ==========================================
# MERGE
# ==========================================

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

master_df.to_csv(
    "data/raw/nifty_1m_master.csv",
    index=False
)

print()
print("=" * 80)
print("MASTER DATASET BUILT")
print("=" * 80)

print(
    "Rows:",
    len(master_df)
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
    "\nSaved:"
)

print(
    "data/raw/nifty_1m_master.csv"
)