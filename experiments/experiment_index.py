from pathlib import Path

import pandas as pd


class ExperimentIndex:
    """
    Central catalog of every AlphaForge experiment.

    Stores one row per experiment.

    Acts as the research database.
    """

    DEFAULT_PATH = Path("experiments/index.csv")

    def __init__(self, path=None):

        self.path = Path(path) if path else self.DEFAULT_PATH

        self.path.parent.mkdir(parents=True, exist_ok=True)

        if self.path.exists():

            self.df = pd.read_csv(self.path)

        else:

            self.df = pd.DataFrame()

    # ==========================================================
    # REGISTER
    # ==========================================================

    def register(self, experiment):

        row = pd.DataFrame([experiment])

        self.df = pd.concat(

            [self.df, row],

            ignore_index=True

        )

        self.save()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(self):

        self.df.to_csv(

            self.path,

            index=False

        )

    # ==========================================================
    # LOAD
    # ==========================================================

    def load(self):

        if self.path.exists():

            self.df = pd.read_csv(self.path)

        return self.df

    # ==========================================================
    # TOP RESULTS
    # ==========================================================

    def top(

        self,

        metric="research_score",

        n=10

    ):

        if self.df.empty:

            return self.df

        return (

            self.df

            .sort_values(

                metric,

                ascending=False

            )

            .head(n)

        )

    # ==========================================================
    # FILTER
    # ==========================================================

    def strategy(

        self,

        strategy_name

    ):

        if self.df.empty:

            return self.df

        return self.df[

            self.df.strategy.str.upper()

            == strategy_name.upper()

        ]

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        print()

        print("=" * 80)

        print("EXPERIMENT INDEX")

        print("=" * 80)

        print()

        print("Experiments :", len(self.df))

        if len(self.df):

            print()

            print(self.top())