def bullish_momentum(data):

    atr = (
        data["Close"]
        .rolling(14)
        .std()
    )

    return (
        (data["Close"] - data["Open"])
        > atr * 0.4
    )

def ema9_above_ema20(data):

    return (
        data["EMA9"]
        >
        data["EMA20"]
    )


def ema20_above_ema50(data):

    return (
        data["EMA20"]
        >
        data["EMA50"]
    )


def price_above_vwap(data):

    return (
        data["Close"]
        >
        data["VWAP"]
    )


def rsi_bullish(data):

    return (
        data["RSI14"]
        >
        50
    )
def bearish_momentum(data):

    atr = (
        data["Close"]
        .rolling(14)
        .std()
    )

    return (
        (data["Open"] - data["Close"])
        > atr * 0.4
    )


FORMULA_REGISTRY = {

    "(close - open) > ATR * 0.4":
        bullish_momentum,

    "(open - close) > ATR * 0.4":
        bearish_momentum,

    "EMA9 > EMA20":
        ema9_above_ema20,

    "EMA20 > EMA50":
        ema20_above_ema50,

    "Close > VWAP":
        price_above_vwap,

    "RSI14 > 50":
        rsi_bullish
}