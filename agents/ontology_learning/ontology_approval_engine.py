from pathlib import Path

import json

from loguru import logger

# ==========================================
# PATHS
# ==========================================
PROPOSAL_DIR = Path(
    "data/ontology_proposals"
)

RULES_FILE = Path(
    "ontology/rule_registry.json"
)

# ==========================================
# LOAD RULES
# ==========================================
with open(
    RULES_FILE,
    "r",
    encoding="utf-8"
) as f:

    rules = json.load(f)

# ==========================================
# APPROVE PROPOSAL
# ==========================================
def approve_proposal(
    proposal_file
):

    with open(
        proposal_file,
        "r",
        encoding="utf-8"
    ) as f:

        proposal = json.load(f)

    concept = proposal["concept"]

    rules[concept] = {

        "logic_type":
        proposal["logic_type"],

        "formula":
        proposal["candidate_formula"]
    }

    logger.success(
        f"Approved concept: "
        f"{concept}"
    )

# ==========================================
# SAVE UPDATED RULES
# ==========================================
def save_rules():

    with open(
        RULES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            rules,
            f,
            indent=4
        )

    logger.success(
        "Ontology registry updated."
    )

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":

    proposal_files = list(
        PROPOSAL_DIR.glob("*.json")
    )

    if len(proposal_files) == 0:

        raise ValueError(
            "No proposals found."
        )

    proposal_file = proposal_files[0]

    approve_proposal(
        proposal_file
    )

    save_rules()