from pathlib import Path

import json
from datetime import datetime

# ==========================================
# OUTPUT FILE
# ==========================================
EXPERIMENT_FILE = Path(
    "experiments/experiment_history.json"
)

# ==========================================
# LOAD HISTORY
# ==========================================
def load_history():

    if not EXPERIMENT_FILE.exists():

        return []

    with open(
        EXPERIMENT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

# ==========================================
# SAVE HISTORY
# ==========================================
def save_history(
    history
):

    with open(
        EXPERIMENT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )

# ==========================================
# TRACK EXPERIMENT
# ==========================================
def track_experiment(
    strategy_name,
    metrics,
    ontology_version="v1"
):

    history = load_history()

    experiment = {

        "timestamp":
        datetime.utcnow().isoformat(),

        "strategy_name":
        strategy_name,

        "ontology_version":
        ontology_version,

        "metrics":
        metrics
    }

    history.append(
        experiment
    )

    save_history(
        history
    )

    return experiment