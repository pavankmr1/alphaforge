from pathlib import Path

import json

# ==========================================
# MEMORY FILE
# ==========================================
MEMORY_FILE = Path(
    "memory/shared_memory.json"
)

# ==========================================
# LOAD MEMORY
# ==========================================
def load_memory():

    if not MEMORY_FILE.exists():

        return {

            "ontology": [],

            "insights": [],

            "failures": [],

            "strategies": []
        }

    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

# ==========================================
# SAVE MEMORY
# ==========================================
def save_memory(
    memory
):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4
        )

# ==========================================
# ADD MEMORY ITEM
# ==========================================
def add_memory(

    category,
    item
):

    memory = load_memory()

    if category not in memory:

        memory[category] = []

    memory[category].append(
        item
    )

    save_memory(
        memory
    )

# ==========================================
# GET MEMORY
# ==========================================
def get_memory(
    category
):

    memory = load_memory()

    return memory.get(
        category,
        []
    )