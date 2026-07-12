from experiments.research_score import ResearchScore


def test_score():

    metrics = {

        "profit_factor": 2.0,

        "win_rate": 0.55,

        "average_rr": 1.2,

        "total_pnl": 1500,

        "total_trades": 80,

    }

    score = ResearchScore.score(metrics)

    assert score > 0

    assert score <= 100