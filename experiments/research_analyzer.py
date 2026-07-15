from typing import Dict

import pandas as pd


class ResearchAnalyzer:
    """
    AlphaForge V3

    Analyzes a collection of experiment results and produces
    quantitative insights.

    This class contains NO trading logic.

    Responsibilities
    ----------------
    - Find best experiment
    - Find worst experiment
    - Measure parameter importance
    - Generate recommendations
    """

    def __init__(

        self,

        experiments: pd.DataFrame

    ):

        self.df = experiments.copy()

    # ==========================================================
    # TOP
    # ==========================================================

    def top(self, n: int = 10):

        return (

            self.df

            .sort_values(

                "research_score",

                ascending=False

            )

            .head(n)

        )
    # ==========================================================
    # BOTTOM
    # ==========================================================

    def bottom(self, n: int = 10):

        return (

            self.df

            .sort_values(

                "research_score",

                ascending=True

            )

            .head(n)

        )

    # ==========================================================
    # BEST CONFIGURATION
    # ==========================================================

    def best_configuration(self):

        return self.top(1).iloc[0].to_dict()

    # ==========================================================
    # WORST CONFIGURATION
    # ==========================================================

    def worst_configuration(self):

        return self.bottom(1).iloc[0].to_dict()


    # ==========================================================
    # BEST
    # ==========================================================

    def best(self):

        return self.top(1).iloc[0]

    # ==========================================================
    # WORST
    # ==========================================================

    def worst(self):

        return self.bottom(1).iloc[0]

    # ==========================================================
    # PARAMETER IMPORTANCE
    # ==========================================================

    def parameter_importance(self):

        ignore = {

            "run_id",

            "research_score",

            "total_trades",

            "wins",

            "losses",

            "win_rate",

            "profit_factor",

            "average_rr",

            "total_pnl",
            "average_winner",

            "average_loser",

            "best_trade_pnl",

            "worst_trade_pnl"

        }

        importance = {}

        for column in self.df.columns:

            if column in ignore:

                continue

            grouped = (

                self.df

                .groupby(column)["research_score"]

                .mean()

            )

            importance[column] = (

                grouped.max()

                -

                grouped.min()

            )

        return dict(

            sorted(

                importance.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )

    # ==========================================================
    # PARAMETER SUMMARY
    # ==========================================================

    def parameter_summary(

        self,

        parameter: str

    ):
        if parameter not in self.df.columns:

            raise ValueError(

                f"Unknown parameter: {parameter}"

            )
        return (

            self.df

            .groupby(parameter)

            .agg(

                average_score=(

                    "research_score",

                    "mean"

                ),

                average_pf=(

                    "profit_factor",

                    "mean"

                ),

                average_rr=(

                    "average_rr",

                    "mean"

                ),

                average_trades=(

                    "total_trades",

                    "mean"

                ),

                average_pnl=(

                    "total_pnl",

                    "mean"

                )

            )

            .reset_index()

            .sort_values(

                "average_score",

                ascending=False

            )

        )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self) -> Dict:

        best = self.best()

        worst = self.worst()

        return {

            "best_run": best["run_id"],

            "best_score": float(best["research_score"]),

            "worst_run": worst["run_id"],

            "worst_score": float(worst["research_score"]),

            "parameter_importance":

                self.parameter_importance()

        }

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    def recommendations(self):

        recommendations = []

        importance = self.parameter_importance()

        for parameter, score in importance.items():

            if score > 15:

                recommendations.append(

                    f"{parameter} has VERY HIGH impact."

                )

            elif score > 5:

                recommendations.append(

                    f"{parameter} has moderate impact."

                )

            else:

                recommendations.append(

                    f"{parameter} has little impact."

                )

        return recommendations