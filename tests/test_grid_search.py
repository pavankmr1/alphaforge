from experiments.grid_search import GridSearch


def test_total_combinations():

    space = {

        "gap_atr": [0.3, 0.5],

        "stop_buffer": [0.25, 0.5],

        "target": ["DAY_HIGH", "PDH"]

    }

    assert (

        GridSearch.total_combinations(space)

        == 8

    )


def test_generate_combinations():

    space = {

        "a": [1, 2],

        "b": [10, 20]

    }

    combos = GridSearch.combinations(space)

    assert len(combos) == 4

    assert {

        "a": 1,

        "b": 10

    } in combos

    assert {

        "a": 2,

        "b": 20

    } in combos