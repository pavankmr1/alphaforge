from copy import deepcopy

import pandas as pd

from experiments.runner import run_experiment
from experiments.research_score import ResearchScore

class ParameterSweep:
    """
    Runs multiple experiments by varying a single parameter.
    """

    def __init__(self, output_root="experiments/runs"):

        self.output_root = output_root

    def run(
        self,
        strategy,
        symbol,
        parameter,
        values,
        start=None,
        end=None,
        base_parameters=None,
    ):

        base_parameters = base_parameters or {}

        results = []

        for value in values:

            params = deepcopy(base_parameters)
            params[parameter] = value

            result = run_experiment(
                strategy_name=strategy,
                symbol=symbol,
                start=start,
                end=end,
                output_root=self.output_root,
                parameters=params,
            )

            metrics = result["metrics"]
            research_score = ResearchScore.score(
                metrics
            )
            score = ResearchScore.score(metrics)

            results.append({

                "parameter": parameter,

                "value": value,

                **metrics,
                "research_score": research_score,

                "run_dir": result["run_dir"]

            })

        return pd.DataFrame(results)