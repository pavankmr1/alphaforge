import pandas as pd


def compute_features(data):

    data = data.copy()
    
    # ==========================================
    # EMAs
    # ==========================================
    data["EMA5"] = (
        data["Close"]
        .ewm(span=5, adjust=False)
        .mean()
    )

    data["EMA9"] = (
        data["Close"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    data["EMA10"] = (
        data["Close"]
        .ewm(span=10, adjust=False)
        .mean()
    )

    data["EMA15"] = (
        data["Close"]
        .ewm(span=15, adjust=False)
        .mean()
    )

    data["EMA20"] = (
        data["Close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    data["EMA21"] = (
        data["Close"]
        .ewm(span=21, adjust=False)
        .mean()
    )

    data["EMA50"] = (
        data["Close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    data["EMA200"] = (
        data["Close"]
        .ewm(span=200, adjust=False)
        .mean()
    )

    # ==========================================
    # SMA
    # ==========================================
    data["SMA18"] = (
        data["Close"]
        .rolling(18)
        .mean()
    )

    data["SMA20"] = (
        data["Close"]
        .rolling(20)
        .mean()
    )

    data["SMA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )

    # ==========================================
    # VWAP
    # ==========================================
    data["VWAP"] = (
        (
            data["Close"]
            * data["Volume"]
        ).cumsum()
        /
        data["Volume"].cumsum()
    )

    # ==========================================
    # ATR14
    # ==========================================
    high_low = (
        data["High"]
        - data["Low"]
    )

    high_close = (
        data["High"]
        - data["Close"].shift()
    ).abs()

    low_close = (
        data["Low"]
        - data["Close"].shift()
    ).abs()

    tr = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)

    data["ATR14"] = (
        tr.rolling(14)
        .mean()
    )

    # ==========================================
    # RSI14
    # ==========================================
    delta = (
        data["Close"]
        .diff()
    )

    gain = (
        delta.where(
            delta > 0,
            0
        )
        .rolling(14)
        .mean()
    )

    loss = (
        -delta.where(
            delta < 0,
            0
        )
        .rolling(14)
        .mean()
    )

    rs = gain / loss

    data["RSI14"] = (
        100
        -
        (
            100
            /
            (1 + rs)
        )
    )

    # ==========================================
    # VOLUME
    # ==========================================
    data["VOL_MA20"] = (
        data["Volume"]
        .rolling(20)
        .mean()
    )

    data["AverageVolume"] = (
        data["Volume"]
        .rolling(20)
        .mean()
    )

    # ==========================================
    # PREVIOUS DAY LEVELS
    # ==========================================
    data["PreviousDayHigh"] = (
        data["High"]
        .shift(1)
    )

    data["PreviousDayLow"] = (
        data["Low"]
        .shift(1)
    )
    data["AsianHigh"] = (
        data["High"]
        .rolling(20)
        .max()
    )

    data["AsianLow"] = (
        data["Low"]
        .rolling(20)
        .min()
    )
    data["LiquidityHigh"] = (
        data["High"]
        .rolling(10)
        .max()
    )

    data["LiquidityLow"] = (
        data["Low"]
        .rolling(10)
        .min()
    )
    # ==========================================
    # FAIR VALUE GAPS (ICT)
    # ==========================================

    data["BullishFVG"] = (

        data["Low"]

        >

        data["High"].shift(2)

    )

    data["BearishFVG"] = (

        data["High"]

        <

        data["Low"].shift(2)

    )

    # ==========================================
    # FVG ZONES
    # ==========================================

    data["BullishFVG_Top"] = (

        data["Low"]

    )

    data["BullishFVG_Bottom"] = (

        data["High"].shift(2)

    )

    data["BullishFVG_Gap"] = (

        data["BullishFVG_Top"]

        -

        data["BullishFVG_Bottom"]

    )

    # ------------------------------------------

    data["BearishFVG_Top"] = (

        data["Low"].shift(2)

    )

    data["BearishFVG_Bottom"] = (

        data["High"]

    )

    data["BearishFVG_Gap"] = (

        data["BearishFVG_Top"]

        -

        data["BearishFVG_Bottom"]

    )

    # ==========================================
    # GAP SIZE VS ATR
    # ==========================================

    data["BullishFVG_GapATR"] = (

        data["BullishFVG_Gap"]

        /

        data["ATR14"]

    )

    data["BearishFVG_GapATR"] = (

        data["BearishFVG_Gap"]

        /

        data["ATR14"]

    )

    # ==========================================
    # QUALITY FVG
    # ==========================================

    data["QUALITY_BULLISH_FVG"] = (

        data["BullishFVG"]

        &

        (data["BullishFVG_GapATR"] >= 0.25)

        &

        (data["BullishFVG_GapATR"] <= 2.0)

    )

    data["QUALITY_BEARISH_FVG"] = (

        data["BearishFVG"]

        &

        (data["BearishFVG_GapATR"] >= 0.25)

        &

        (data["BearishFVG_GapATR"] <= 2.0)

    )
    data["PreviousClose"] = (
        data["Close"]
        .shift(1)
    )

    # ==========================================
    # PIVOT
    # ==========================================
    data["Pivot"] = (
        data["PreviousDayHigh"]
        +
        data["PreviousDayLow"]
        +
        data["PreviousClose"]
    ) / 3

    # ==========================================
    # SIMPLE PRICE ALIASES
    # ==========================================
    data["Price"] = data["Close"]
    data["Market"] = data["Close"]
    data["Trend"] = data["Close"]
    data["PreviousHigh"] = data["High"].shift(1)

    data["PreviousLow"] = data["Low"].shift(1)
    from backtesting.support_resistance import (
        add_support_resistance
    )

    data = add_support_resistance(
        data
    )
    from backtesting.smc_features import (
        add_smc_features
    )

    data = add_smc_features(data)
    # ==========================================
    # CANDLE FEATURES
    # ==========================================

    data["GREEN_CANDLE"] = (
        data["Close"]
        >
        data["Open"]
    )

    data["RED_CANDLE"] = (
        data["Close"]
        <
        data["Open"]
    )

    # ==========================================
    # CONSECUTIVE GREEN CANDLES
    # ==========================================

    data["CONSEC_GREEN_2"] = (

        data["GREEN_CANDLE"]

        &

        data["GREEN_CANDLE"].shift(1)

    )

    data["CONSEC_GREEN_3"] = (

        data["GREEN_CANDLE"]

        &

        data["GREEN_CANDLE"].shift(1)

        &

        data["GREEN_CANDLE"].shift(2)

    )

    # ==========================================
    # CONSECUTIVE RED CANDLES
    # ==========================================

    data["CONSEC_RED_2"] = (

        data["RED_CANDLE"]

        &

        data["RED_CANDLE"].shift(1)

    )

    data["CONSEC_RED_3"] = (

        data["RED_CANDLE"]

        &

        data["RED_CANDLE"].shift(1)

        &

        data["RED_CANDLE"].shift(2)

    )

    # ==========================================
    # WICK FEATURES
    # ==========================================

    body = (
        data["Close"]
        -
        data["Open"]
    ).abs()

    lower_wick = (

        data[
            ["Open", "Close"]
        ]
        .min(axis=1)

        -

        data["Low"]

    )

    upper_wick = (

        data["High"]

        -

        data[
            ["Open", "Close"]
        ]
        .max(axis=1)

    )

    data["LONG_LOWER_WICK"] = (

        lower_wick

        >

        body * 1.5

    )

    data["LONG_UPPER_WICK"] = (

        upper_wick

        >

        body * 1.5

    )

    # ==========================================
    # SWING POINTS
    # ==========================================

    data["SWING_HIGH"] = (

        (data["High"] > data["High"].shift(1))

        &

        (data["High"] > data["High"].shift(-1))

    )

    data["SWING_LOW"] = (

        (data["Low"] < data["Low"].shift(1))

        &

        (data["Low"] < data["Low"].shift(-1))

    )

    data["LAST_SWING_HIGH"] = (

        data["High"]
        .where(
            data["SWING_HIGH"]
        )
        .ffill()

    )

    data["LAST_SWING_LOW"] = (

        data["Low"]
        .where(
            data["SWING_LOW"]
        )
        .ffill()

    )

    # ==========================================
    # LIQUIDITY SWEEPS (FIRST BREAK ONLY)
    # ==========================================

    # ==========================================
    # LIQUIDITY SWEEPS V3
    # ==========================================

    data["SWEEP_SWING_LOW"] = (

        (
            data["Low"]
            <
            data["LAST_SWING_LOW"].shift(1)
        )

        &

        (
            data["Low"].shift(1)
            >=
            data["LAST_SWING_LOW"].shift(1)
        )

    )

    data["SWEEP_SWING_HIGH"] = (

        (
            data["High"]
            >
            data["LAST_SWING_HIGH"].shift(1)
        )

        &

        (
            data["High"].shift(1)
            <=
            data["LAST_SWING_HIGH"].shift(1)
        )

    )

    # ==========================================
    # BREAK OF STRUCTURE
    # ==========================================

    data["BOS_BULLISH"] = (

        (
            data["Close"]
            >
            data["LAST_SWING_HIGH"].shift(1)
        )

        &

        (
            data["Close"].shift(1)
            <=
            data["LAST_SWING_HIGH"].shift(1)
        )

    )

    data["BOS_BEARISH"] = (

        (
            data["Close"]
            <
            data["LAST_SWING_LOW"].shift(1)
        )

        &

        (
            data["Close"].shift(1)
            >=
            data["LAST_SWING_LOW"].shift(1)
        )

    )

   
    # ==========================================
    # LIQUIDITY REJECTION
    # ==========================================

    data["BULLISH_SWEEP_REJECTION"] = (

        data["SWEEP_SWING_LOW"]

        &

        data["LONG_LOWER_WICK"]

    )

    data["BEARISH_SWEEP_REJECTION"] = (

        data["SWEEP_SWING_HIGH"]

        &

        data["LONG_UPPER_WICK"]

    )
    # ==========================================
    # CONFIRMATION CANDLES
    # ==========================================

    data["BULLISH_CONFIRMATION"] = (

        (data["Close"] > data["Open"])

        &

        (
            (data["Close"] - data["Open"])
            >
            data["ATR14"] * 0.5
        )

    )

    data["BEARISH_CONFIRMATION"] = (

        (data["Close"] < data["Open"])

        &

        (
            (data["Open"] - data["Close"])
            >
            data["ATR14"] * 0.5
        )

    )

     # ==========================================
    # STRONG BOS
    # ==========================================

    data["STRONG_BOS_BULLISH"] = (

        data["BOS_BULLISH"]

        &

        data["BULLISH_CONFIRMATION"]

    )

    data["STRONG_BOS_BEARISH"] = (

        data["BOS_BEARISH"]

        &

        data["BEARISH_CONFIRMATION"]

    )

    # ==========================================
    # REACTION ZONE PROTOTYPE
    # ==========================================

    data["PREV_BEARISH_HIGH"] = (

        data["High"]
        .where(
            data["RED_CANDLE"]
        )
        .ffill()

    )

    data["PREV_BEARISH_LOW"] = (

        data["Low"]
        .where(
            data["RED_CANDLE"]
        )
        .ffill()

    )

    
    # ==========================================
    # MARKET STRUCTURE
    # ==========================================

    data["HIGHER_HIGH"] = (
        data["High"]
        >
        data["High"].shift(1)
    )

    data["HIGHER_LOW"] = (
        data["Low"]
        >
        data["Low"].shift(1)
    )

    data["LOWER_HIGH"] = (
        data["High"]
        <
        data["High"].shift(1)
    )

    data["LOWER_LOW"] = (
        data["Low"]
        <
        data["Low"].shift(1)
    )

    data["BULLISH_STRUCTURE"] = (

        data["HIGHER_HIGH"]

        &

        data["HIGHER_LOW"]

    ).fillna(False).astype(bool)


    data["BEARISH_STRUCTURE"] = (

        data["LOWER_HIGH"]

        &

        data["LOWER_LOW"]

    ).fillna(False).astype(bool)

    # ==========================================
    # TREND V2
    # ==========================================

    data["BULLISH_TREND_V2"] = (

        (data["EMA20"] > data["EMA50"])

        &

        data["BULLISH_STRUCTURE"]

    )

    data["BEARISH_TREND_V2"] = (

        (data["EMA20"] < data["EMA50"])

        &

        data["BEARISH_STRUCTURE"]

    )

    # ==================================
    # RECENT LIQUIDITY SWEEP
    # ==================================

    data["RECENT_SWEEP"] = (

        data["SWEEP_SWING_LOW"]

        .rolling(5)

        .max()

        .fillna(False)

        .astype(bool)

    )

    return data