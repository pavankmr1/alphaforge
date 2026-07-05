from datetime import datetime

from experiments.walk_forward import (
    build_walk_forward_windows,
    create_walk_forward_dir,
)


def test_build_walk_forward_windows_rolls_forward_by_test_period():
    windows = build_walk_forward_windows(
        start="2024-01-01",
        end="2024-07-01",
        train_months=3,
        test_months=1,
    )

    assert windows == [
        {
            "train_start": "2024-01-01",
            "train_end": "2024-04-01",
            "test_start": "2024-04-01",
            "test_end": "2024-05-01",
        },
        {
            "train_start": "2024-02-01",
            "train_end": "2024-05-01",
            "test_start": "2024-05-01",
            "test_end": "2024-06-01",
        },
        {
            "train_start": "2024-03-01",
            "train_end": "2024-06-01",
            "test_start": "2024-06-01",
            "test_end": "2024-07-01",
        },
    ]


def test_create_walk_forward_dir_increments_on_collision(tmp_path):
    now = datetime(2026, 7, 5, 9, 30)

    first = create_walk_forward_dir(tmp_path, now=now)
    second = create_walk_forward_dir(tmp_path, now=now)

    assert first.name == "walk_forward_2026-07-05_093000"
    assert second.name == "walk_forward_2026-07-05_093000_2"
