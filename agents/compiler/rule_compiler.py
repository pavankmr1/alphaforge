from pathlib import Path
from loguru import logger

import json

from compiler_rules import RULE_MAPPINGS

# ==========================================
# PATHS
# ==========================================
INPUT_DIR = Path(
    "data/parsed_strategies"
)

OUTPUT_DIR = Path(
    "data/compiled_strategies"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# LOGGING
# ==========================================
logger.add(
    "logs/alphaforge.log",
    rotation="10 MB"
)

# ==========================================
# MATCH RULES
# ==========================================
def find_rule(condition_text: str):

    condition_lower = condition_text.lower()

    matched_rules = []

    for phrase, rule_data in RULE_MAPPINGS.items():

        if phrase in condition_lower:

            matched_rules.append({

                "matched_phrase": phrase,

                "logic_type":
                rule_data["logic_type"],

                "formula":
                rule_data["formula"]
            })

    return matched_rules

# ==========================================
# COMPILE STRATEGY
# ==========================================
def compile_strategy(strategy_data):

    compiled_conditions = []

    entry_conditions = strategy_data.get(
        "entry_conditions",
        []
    )

    for condition in entry_conditions:

        matched_rules = find_rule(
            condition
        )

        compiled_conditions.append({

            "original_condition":
            condition,

            "compiled_logic":
            matched_rules
        })

    strategy_data[
        "compiled_entry_logic"
    ] = compiled_conditions

    return strategy_data

# ==========================================
# PROCESS JSON FILES
# ==========================================
def process_strategies():

    json_files = INPUT_DIR.glob(
        "*.json"
    )

    for json_file in json_files:

        try:

            logger.info(
                f"Compiling: {json_file.name}"
            )

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:

                strategy_data = json.load(f)

            compiled_strategy = compile_strategy(
                strategy_data
            )

            output_file = (
                OUTPUT_DIR /
                json_file.name
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    compiled_strategy,
                    f,
                    indent=4
                )

            logger.success(
                f"Compiled strategy saved: "
                f"{output_file.name}"
            )

        except Exception as e:

            logger.error(
                f"Failed compiling "
                f"{json_file.name}: {e}"
            )

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":

    process_strategies()