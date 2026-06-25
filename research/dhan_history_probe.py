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

response = dhan.intraday_minute_data(
    security_id="13",
    exchange_segment="IDX_I",
    instrument_type="INDEX",
    from_date="2026-03-01",
    to_date="2026-05-29"
)

print(response.keys())

print("\nFULL RESPONSE")
print("=" * 60)

print(response)

print("\nDATA TYPE")
print(type(response["data"]))

print(response["status"])
print(response["remarks"])
print("\nDATA")
print(response["data"])
if "data" in response:
    df = pd.DataFrame({
        "timestamp": response["data"]["timestamp"],
        "open": response["data"]["open"],
        "high": response["data"]["high"],
        "low": response["data"]["low"],
        "close": response["data"]["close"],
        "volume": response["data"]["volume"]
    })