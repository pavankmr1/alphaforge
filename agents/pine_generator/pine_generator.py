from pathlib import Path
from loguru import logger

import json

# ==========================================
# PATHS
# ==========================================
INPUT_DIR = Path(
    "data/compiled_strategies"
)

OUTPUT_DIR = Path(
    "data/generated_pines"
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
# GENERATE CONDITIONS
# ==========================================
def generate_conditions(compiled_logic):

    pine_conditions = []

    for item in compiled_logic:

        compiled_rules = item.get(
            "compiled_logic",
            []
        )

        for rule in compiled_rules:

            formula = rule.get(
                "formula"
            )

            pine_conditions.append(
                formula
            )

    return pine_conditions

# ==========================================
# GENERATE PINE SCRIPT
# ==========================================
def generate_pine(strategy_data):

    strategy_name = strategy_data.get(
        "name",
        "AlphaForge Strategy"
    )

    compiled_logic = strategy_data.get(
        "compiled_entry_logic",
        []
    )

    conditions = generate_conditions(
        compiled_logic
    )

    combined_conditions = " and \n".join(
        conditions
    )

    pine_script = f'''
//@version=5
strategy(
    "{strategy_name}",
    overlay=true
)

// ==========================================
// INDICATORS
// ==========================================
atr = ta.atr(14)

// ==========================================
// ENTRY CONDITIONS
// ==========================================
longCondition =
{combined_conditions}

// ==========================================
// ENTRIES
// ==========================================
if longCondition

    strategy.entry(
        "LONG",
        strategy.long
    )
'''

    return pine_script

# ==========================================
# PROCESS STRATEGIES
# ==========================================
def process_strategies():

    json_files = INPUT_DIR.glob(
        "*.json"
    )

    for json_file in json_files:

        try:

            logger.info(
                f"Generating Pine: "
                f"{json_file.name}"
            )

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as f:

                strategy_data = json.load(f)

            pine_script = generate_pine(
                strategy_data
            )

            output_file = (
                OUTPUT_DIR /
                f"{json_file.stem}.pine"
            )

            output_file.write_text(
                pine_script,
                encoding="utf-8"
            )

            logger.success(
                f"Pine generated: "
                f"{output_file.name}"
            )

        except Exception as e:

            logger.error(
                f"Failed generating Pine "
                f"for {json_file.name}: {e}"
            )

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":

    process_strategies()