import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.session_engine import (
    get_session_id
)

from backtesting.setup_engine_v2 import (
    build_bullish_setup_v2
)

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

context_df = build_context(data)

session_ids = get_session_id(
    data.index
)

setup = build_bullish_setup_v2(

    session_ids=session_ids,

    context=context_df[
        "BULLISH_CONTEXT"
    ],

    sweep=data[
        "SWEEP_SWING_LOW"
    ],

    rejection=data[
        "LONG_LOWER_WICK"
    ],

    confirmation=data[
        "BULLISH_CONFIRMATION"
    ]
)

print()
print("=" * 60)
print("SETUP ENGINE V2")
print("=" * 60)

print(
    "Setups:",
    int(setup.sum())
)

print()

print(
    setup[
        setup
    ].index[:50]
)