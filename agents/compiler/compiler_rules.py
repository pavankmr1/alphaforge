from pathlib import Path
import json

RULES_FILE = Path(
    "ontology/rule_registry.json"
)

with open(
    RULES_FILE,
    "r",
    encoding="utf-8"
) as f:

    RULE_MAPPINGS = json.load(f)