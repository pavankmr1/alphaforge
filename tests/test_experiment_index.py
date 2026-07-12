from experiments.experiment_index import ExperimentIndex


def test_register(tmp_path):

    index_file = tmp_path / "index.csv"

    index = ExperimentIndex(index_file)

    index.register({

        "run_id": "001",

        "strategy": "UNICORN",

        "research_score": 88.2

    })

    assert len(index.df) == 1

    assert index.df.iloc[0]["run_id"] == "001"