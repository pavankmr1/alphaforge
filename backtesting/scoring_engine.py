import pandas as pd


def bullish_score(data, context):

    score = pd.Series(
        0,
        index=data.index
    )

    score += (
        context["BULLISH_CONTEXT"]
        .astype(int) * 3
    )

    score += (
        data["BULLISH_STRUCTURE"]
        .astype(int) * 2
    )

    score += (
        data["STRONG_BOS_BULLISH"]
        .astype(int) * 2
    )

    score += (
        data["BULLISH_CONFIRMATION"]
        .astype(int) * 1
    )

    score += (
        data["SWEEP_SWING_LOW"]
        .astype(int) * 1
    )

    return score