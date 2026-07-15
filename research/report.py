from pathlib import Path

import pandas as pd

from experiments.research_analyzer import ResearchAnalyzer
from experiments.strategy_report import StrategyReport


INDEX_FILE = Path("experiments/index.csv")


def load_index():

    if not INDEX_FILE.exists():

        raise FileNotFoundError(

            f"Missing experiment index: {INDEX_FILE}"

        )

    return pd.read_csv(INDEX_FILE)


def main():

    df = load_index()

    analyzer = ResearchAnalyzer(df)

    report = StrategyReport(analyzer)

    report.print_report()

    output = Path("experiments/strategy_report.txt")

    report.save(output)

    print()

    print("=" * 80)

    print(

        f"Report saved to {output}"

    )

    print("=" * 80)

    print()


if __name__ == "__main__":

    main()