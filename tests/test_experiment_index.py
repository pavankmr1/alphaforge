from experiments.experiment_index import ExperimentIndex


def test_register():

    index = ExperimentIndex("tests/tmp_index.csv")

    index.register({

        "run_id": "001",

        "strategy": "UNICORN",

        "research_score": 88.2

    })

    assert len(index.df) == 1