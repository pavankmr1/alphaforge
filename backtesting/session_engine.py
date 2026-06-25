import pandas as pd


def get_session_id(index):

    return pd.Series(
        index.date,
        index=index
    )