from experiments.research_engine import ResearchEngine


def test_engine_initialization():

    engine = ResearchEngine()

    assert engine.runner is not None

    assert engine.walk_forward is not None

    assert engine.monte_carlo is not None

    assert engine.comparison is not None