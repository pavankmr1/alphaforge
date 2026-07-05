from datetime import datetime

from experiments.runner import create_run_dir, save_json


def test_create_run_dir_increments(tmp_path):
    now = datetime(2026, 7, 5)

    first = create_run_dir(tmp_path, now=now)
    second = create_run_dir(tmp_path, now=now)

    assert first.name == "2026-07-05_001"
    assert second.name == "2026-07-05_002"


def test_save_json_serializes_datetimes(tmp_path):
    path = tmp_path / "payload.json"

    save_json(
        path,
        {
            "created_at": datetime(2026, 7, 5, 9, 30),
        },
    )

    assert "2026-07-05T09:30:00" in path.read_text()
