import pandas as pd

from experiments.parameter_sweep import ParameterSweep


def test_parameter_sweep_runs():

    sweep = ParameterSweep()

    df = sweep.run(

        strategy="UNICORN",

        symbol="nifty",

        parameter="min_gap_atr",

        values=[0.5],

        start="2025-01-01",

        end="2025-01-02",

    )

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 1

    assert "profit_factor" in df.columns