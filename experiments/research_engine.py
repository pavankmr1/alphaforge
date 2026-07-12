from pathlib import Path

from loguru import logger

from experiments.runner import run_experiment
from experiments.comparison_engine import (
    compare_runs,
    rank_runs,
)
from experiments.walk_forward import run_walk_forward
from experiments.monte_carlo import run_monte_carlo


class ResearchEngine:
    """
    AlphaForge Research Engine

    High-level orchestration layer for research workflows.
    """

    def __init__(self, output_root="experiments/runs"):

        self.output_root = Path(output_root)

        logger.info("Research Engine initialized.")

    # ======================================================
    # Experiment
    # ======================================================

    def run_experiment(self, **kwargs):

        kwargs.setdefault("output_root", self.output_root)

        return run_experiment(**kwargs)

    # ======================================================
    # Walk Forward
    # ======================================================

    def run_walk_forward(self, **kwargs):

        kwargs.setdefault("output_root", self.output_root)

        return run_walk_forward(**kwargs)

    # ======================================================
    # Monte Carlo
    # ======================================================

    def run_monte_carlo(self, **kwargs):

        return run_monte_carlo(**kwargs)

    # ======================================================
    # Ranking
    # ======================================================

    def leaderboard(self):

        return rank_runs(self.output_root)

    # ======================================================
    # Compare
    # ======================================================

    def compare(self, run_a, run_b):

        return compare_runs(run_a, run_b)

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        print()

        print("=" * 80)
        print("ALPHAFORGE RESEARCH ENGINE")
        print("=" * 80)
        print()

        print("Output Root :", self.output_root)

        print()

        print("Capabilities")

        print("- Experiment Runner")
        print("- Walk Forward")
        print("- Monte Carlo")
        print("- Leaderboard")
        print("- Experiment Comparison")