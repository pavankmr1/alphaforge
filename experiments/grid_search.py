from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd

from experiments.runner import run_experiment
from experiments.research_score import ResearchScore


class GridSearch:
    """
    AlphaForge V3

    Performs exhaustive multi-parameter optimization using
    Cartesian product search.

    Every parameter combination is executed as an independent
    experiment through the Experiment Runner.
    """

    def __init__(self):

        self.results = []

    # ==========================================================
    # RUN
    # ==========================================================

    def run(
        self,
        strategy: str,
        symbol: str,
        start: str,
        end: str,
        parameter_space: dict[str, list[Any]],
        output_root="experiments/runs",
    ) -> pd.DataFrame:

        self.results = []

        parameter_names = list(parameter_space.keys())

        parameter_values = list(parameter_space.values())

        for values in product(*parameter_values):

            config = dict(

                zip(
                    parameter_names,
                    values,
                )

            )

            result = run_experiment(

                strategy_name=strategy,

                symbol=symbol,

                start=start,

                end=end,

                parameters=config,

                output_root=output_root,

            )

            metrics = result["metrics"]

            research_score = ResearchScore.score(
                metrics
            )

            row = {

                "run_id": Path(

                    result["run_dir"]

                ).name,

                "research_score": research_score,

                "total_trades": metrics["total_trades"],

                "wins": metrics["wins"],

                "losses": metrics["losses"],

                "win_rate": metrics["win_rate"],

                "profit_factor": metrics["profit_factor"],

                "average_rr": metrics["average_rr"],

                "total_pnl": metrics["total_pnl"],

            }

            row.update(config)

            self.results.append(row)

        df = pd.DataFrame(

            self.results

        )

        if df.empty:

            return df

        return df.sort_values(

            by="research_score",

            ascending=False,

            ignore_index=True,

        )

    # ==========================================================
    # COMBINATIONS
    # ==========================================================

    @staticmethod
    def combinations(
        parameter_space: dict[str, list[Any]]
    ) -> list[dict[str, Any]]:
        """
        Returns every parameter combination without
        running experiments.
        """

        keys = list(parameter_space.keys())

        values = list(parameter_space.values())

        return [

            dict(zip(keys, combo))

            for combo in product(*values)

        ]

    # ==========================================================
    # COUNT
    # ==========================================================

    @staticmethod
    def total_combinations(
        parameter_space: dict[str, list[Any]]
    ) -> int:
        """
        Returns the total number of parameter combinations.
        """

        total = 1

        for values in parameter_space.values():

            total *= len(values)

        return total