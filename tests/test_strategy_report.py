import pandas as pd

from experiments.research_analyzer import ResearchAnalyzer
from experiments.strategy_report import StrategyReport


def test_report_build():

    df = pd.DataFrame({

        "run_id": [

            "1",

            "2"

        ],

        "research_score": [

            90,

            50

        ],

        "profit_factor": [

            2,

            1

        ],

        "average_rr": [

            1,

            0.5

        ],

        "total_pnl": [

            100,

            50

        ],

        "total_trades": [

            10,

            10

        ],

        "wins": [

            7,

            4

        ],

        "losses": [

            3,

            6

        ],

        "gap": [

            0.5,

            0.3

        ]

    })

    analyzer = ResearchAnalyzer(df)

    report = StrategyReport(analyzer)

    data = report.build()

    assert "best" in data

    assert "worst" in data

    assert "importance" in data

    assert "recommendations" in data