import pandas as pd

from experiments.research_analyzer import ResearchAnalyzer
def test_parameter_summary():

    df = pd.DataFrame({

        "research_score":[50,60,70],

        "profit_factor":[1,2,3],

        "average_rr":[1,1,1],

        "total_trades":[10,20,30],

        "total_pnl":[100,200,300],

        "gap":[0.3,0.3,0.5]

    })

    analyzer = ResearchAnalyzer(df)

    summary = analyzer.parameter_summary("gap")

    assert len(summary) == 2

def test_parameter_importance():

    df = pd.DataFrame({

        "run_id": [

            "1",

            "2",

            "3"

        ],

        "research_score": [

            50,

            70,

            90

        ],

        "gap": [

            0.3,

            0.5,

            0.7

        ],

        "trend": [

            True,

            True,

            False

        ]

    })

    analyzer = ResearchAnalyzer(df)

    importance = analyzer.parameter_importance()

    assert "gap" in importance

    assert "trend" in importance