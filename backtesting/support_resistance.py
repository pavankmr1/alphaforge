def add_support_resistance(
    data,
    lookback=20
):

    data = data.copy()

    data["Support"] = (

        data["Low"]
        .rolling(lookback)
        .min()
    )

    data["Resistance"] = (

        data["High"]
        .rolling(lookback)
        .max()
    )

    return data