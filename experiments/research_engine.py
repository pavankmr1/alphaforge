from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from experiments.runner import ExperimentRunner
from experiments.comparison_engine import ComparisonEngine
from experiments.walk_forward import WalkForwardRunner
from experiments.monte_carlo import MonteCarloAnalyzer


class ResearchEngine:
    """
    AlphaForge V3

    Central coordinator for all quantitative research.

    Responsibilities
    ----------------
    - Run experiments
    - Parameter optimization
    - Walk-forward validation
    - Monte Carlo validation
    - Compare experiments
    - Build research leaderboard

    This class SHOULD NOT contain trading logic.
    """

    def __init__(

        self,

        output_root: str = "experiments/runs"

    ):

        self.output_root = Path(output_root)

        self.runner = ExperimentRunner(

            output_root=self.output_root

        )

        self.comparison = ComparisonEngine()

        self.walk_forward = WalkForwardRunner()

        self.monte_carlo = MonteCarloAnalyzer()

        logger.info(

            "Research Engine initialized."

        )

    # ======================================================
    # Experiment
    # ======================================================

    def run_experiment(

        self,

        **kwargs

    ):

        logger.info(

            "Running experiment..."

        )

        return self.runner.run(

            **kwargs

        )

    # ======================================================
    # Walk Forward
    # ======================================================

    def run_walk_forward(

        self,

        **kwargs

    ):

        logger.info(

            "Running walk-forward..."

        )

        return self.walk_forward.run(

            **kwargs

        )

    # ======================================================
    # Monte Carlo
    # ======================================================

    def run_monte_carlo(

        self,

        **kwargs

    ):

        logger.info(

            "Running Monte Carlo..."

        )

        return self.monte_carlo.run(

            **kwargs

        )

    # ======================================================
    # Compare
    # ======================================================

    def compare(

        self,

        experiment_paths: List[str]

    ):

        logger.info(

            "Comparing experiments..."

        )

        return self.comparison.compare(

            experiment_paths

        )

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        print()

        print("=" * 80)

        print("ALPHAFORGE V3 RESEARCH ENGINE")

        print("=" * 80)

        print()

        print("Output Root")

        print(self.output_root)

        print()

        print("Modules")

        print("- Experiment Runner")

        print("- Walk Forward")

        print("- Monte Carlo")

        print("- Comparison Engine")