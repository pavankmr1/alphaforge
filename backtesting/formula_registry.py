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
        bearish_momentum
}