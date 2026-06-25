import pandas as pd


# ============================================================
# GET CHILD CANDLES
# ============================================================

def find_child_candles(
    df_lower,
    parent_time,
    minutes=5
):
    """
    Returns all lower timeframe candles
    inside one higher timeframe candle.
    """

    start = parent_time

    end = (
        parent_time
        + pd.Timedelta(minutes=minutes)
    )

    return df_lower.loc[
        (df_lower.index >= start)
        &
        (df_lower.index < end)
    ]


# ============================================================
# FIND LOWER TF FVGs
# ============================================================

def find_lower_tf_fvgs(
    df_window,
    bullish=True,
    quality_only=True
):
    """
    Returns all FVGs inside a lower timeframe window.
    """

    if bullish:

        if quality_only:

            return df_window[
                df_window["QUALITY_BULLISH_FVG"]
            ]

        return df_window[
            df_window["BullishFVG"]
        ]

    else:

        if quality_only:

            return df_window[
                df_window["QUALITY_BEARISH_FVG"]
            ]

        return df_window[
            df_window["BearishFVG"]
        ]


# ============================================================
# SELECT LATEST VALID FVG
# ============================================================

def select_latest_fvg(
    fvg_df
):
    """
    ICT prefers the newest imbalance.
    """

    if len(fvg_df) == 0:

        return None

    return fvg_df.iloc[-1]


# ============================================================
# BUILD FVG OBJECT
# ============================================================

def build_fvg_object(
    row,
    bullish=True
):
    """
    Standard FVG dictionary used
    throughout AlphaForge.
    """

    if bullish:

        return {

            "direction": "bullish",

            "created": row.name,

            "top": row["BullishFVG_Top"],

            "bottom": row["BullishFVG_Bottom"],

            "gap": row["BullishFVG_Gap"],

            "gap_atr": row["BullishFVG_GapATR"],

            "valid": True,

            "mitigated": False,

            "broken": False

        }

    return {

        "direction": "bearish",

        "created": row.name,

        "top": row["BearishFVG_Top"],

        "bottom": row["BearishFVG_Bottom"],

        "gap": row["BearishFVG_Gap"],

        "gap_atr": row["BearishFVG_GapATR"],

        "valid": True,

        "mitigated": False,

        "broken": False

    }


# ============================================================
# CHECK FVG RETEST
# ============================================================

def is_fvg_retested(
    candle,
    fvg
):
    """
    Candle taps the imbalance.
    """

    return (

        candle["Low"]
        <=
        fvg["top"]

        and

        candle["Low"]
        >=
        fvg["bottom"]

    )


# ============================================================
# CHECK FVG BREAK
# ============================================================

def is_fvg_invalidated(
    candle,
    fvg
):
    """
    Bullish FVG invalidation.

    Close below bottom.
    """

    return (

        candle["Close"]
        <
        fvg["bottom"]

    )


# ============================================================
# UPDATE ACTIVE FVG LIST
# ============================================================

def update_active_fvgs(
    active_fvgs,
    candle
):
    """
    Removes broken FVGs.
    """

    updated = []

    for fvg in active_fvgs:

        if is_fvg_invalidated(
            candle,
            fvg
        ):

            continue

        updated.append(
            fvg
        )

    return updated


# ============================================================
# REPLACE WITH NEWER FVG
# ============================================================

def add_new_fvg(
    active_fvgs,
    new_fvg
):
    """
    Adds newest FVG.

    We will later improve this
    with hierarchy rules.
    """

    active_fvgs.append(
        new_fvg
    )

    active_fvgs = sorted(

        active_fvgs,

        key=lambda x: x["created"]

    )

    return active_fvgs