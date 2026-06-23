from dhanhq import dhanhq
import pandas as pd

from dhanhq import DhanContext
from dhanhq import dhanhq

from dhanhq import DhanContext, dhanhq
import pandas as pd

from dotenv import load_dotenv

import os



# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()

YOUR_CLIENT_ID = os.getenv(
    "DHAN_CLIENT_ID"
)
YOUR_NEW_TOKEN = os.getenv(
    "DHAN_ACCESS_TOKEN"
)


context = DhanContext(
    client_id=YOUR_CLIENT_ID,
    access_token=YOUR_NEW_TOKEN
)
dhan = dhanhq(context)

# ============================================
# CONFIG
# ============================================


# CONNECT
# ============================================

# dhan = dhanhq(
#     CLIENT_ID,
#     ACCESS_TOKEN
# )

print("\n" + "=" * 60)
print("DHAN CONNECTION SUCCESS")
print("=" * 60)

# ============================================
# NIFTY INDEX SECURITY ID
# ============================================

SECURITY_ID = "13"  # NIFTY 50

# ============================================
# FETCH DATA
# ============================================

response = dhan.intraday_minute_data(
    security_id=SECURITY_ID,
    exchange_segment="IDX_I",
    instrument_type="INDEX",
    from_date="2026-05-01",
    to_date="2026-06-24"
)

print("\n" + "=" * 60)
print("RAW RESPONSE")
print("=" * 60)

print(response)

# ============================================
# SAVE DATA
# ============================================

if "data" in response:

    df = pd.DataFrame(response["data"])

    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)

    print(df.head())

    print("\nRows:", len(df))

    if len(df) > 0:

        print(
            "Start:",
            df.iloc[0]
        )

        print(
            "End:",
            df.iloc[-1]
        )

    df.to_csv(
        "data/nifty_1m_dhan.csv",
        index=False
    )

    print(
        "\nSaved:",
        "data/nifty_1m_dhan.csv"
    )

else:

    print(
        "\nNo data returned."
    )