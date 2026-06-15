from pathlib import Path
import json

from ontology.compiler import (
    compile_strategy
)

INPUT_DIR = Path(
    "data/parsed_strategies"
)

OUTPUT_DIR = Path(
    "data/compiled_strategies_v2"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

files = list(
    INPUT_DIR.glob("*.json")
)

print(
    f"\nFound {len(files)} strategies"
)

for file in files:

    print(
        f"\nCompiling: {file.name}"
    )

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        strategy = json.load(f)

    compiled = compile_strategy(
        strategy
    )

    output_file = (
        OUTPUT_DIR /
        file.name
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            compiled,
            f,
            indent=4
        )

print(
    "\nCorpus compilation completed."
)