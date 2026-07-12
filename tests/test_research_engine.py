from experiments.research_engine import ResearchEngine


def test_engine_initialization():

    engine = ResearchEngine()

    assert engine.output_root is not None


def test_engine_has_api():

    engine = ResearchEngine()

    assert callable(engine.run_experiment)

    assert callable(engine.run_walk_forward)

    assert callable(engine.run_monte_carlo)

    assert callable(engine.leaderboard)

    assert callable(engine.compare)