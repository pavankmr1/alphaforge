from pathlib import Path

from experiments.research_analyzer import ResearchAnalyzer


class StrategyReport:
    """
    AlphaForge V3

    Generates a deterministic strategy research report.

    Responsibilities
    ----------------
    - Best configuration
    - Worst configuration
    - Parameter importance
    - Recommendations
    - Console report
    """

    def __init__(

        self,

        analyzer: ResearchAnalyzer

    ):

        self.analyzer = analyzer

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(self):

        return {

            "best": self.analyzer.best_configuration(),

            "worst": self.analyzer.worst_configuration(),

            "importance": self.analyzer.parameter_importance(),

            "recommendations": self.analyzer.recommendations()

        }

    # ==========================================================
    # PRINT
    # ==========================================================

    def print_report(self):

        report = self.build()

        best = report["best"]

        worst = report["worst"]

        print()

        print("=" * 80)

        print("ALPHAFORGE STRATEGY REPORT")

        print("=" * 80)

        print()

        print("BEST CONFIGURATION")

        print("-" * 80)

        for key, value in best.items():

            print(f"{key:<20}: {value}")

        print()

        print("WORST CONFIGURATION")

        print("-" * 80)

        for key, value in worst.items():

            print(f"{key:<20}: {value}")

        print()

        print("PARAMETER IMPORTANCE")

        print("-" * 80)

        for parameter, score in report["importance"].items():

            print(

                f"{parameter:<20}: {score:.2f}"

            )

        print()

        print("RECOMMENDATIONS")

        print("-" * 80)

        for recommendation in report["recommendations"]:

            print(

                f"• {recommendation}"

            )

        print()

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(

        self,

        path

    ):

        path = Path(path)

        report = self.build()

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            f.write("=" * 80 + "\n")

            f.write("ALPHAFORGE STRATEGY REPORT\n")

            f.write("=" * 80 + "\n\n")

            f.write("BEST CONFIGURATION\n")

            f.write("-" * 80 + "\n")

            for k, v in report["best"].items():

                f.write(f"{k}: {v}\n")

            f.write("\n")

            f.write("WORST CONFIGURATION\n")

            f.write("-" * 80 + "\n")

            for k, v in report["worst"].items():

                f.write(f"{k}: {v}\n")

            f.write("\n")

            f.write("PARAMETER IMPORTANCE\n")

            f.write("-" * 80 + "\n")

            for k, v in report["importance"].items():

                f.write(f"{k}: {v:.2f}\n")

            f.write("\n")

            f.write("RECOMMENDATIONS\n")

            f.write("-" * 80 + "\n")

            for r in report["recommendations"]:

                f.write(f"- {r}\n")