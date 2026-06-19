from pathlib import Path
import json

RULES_FILE = Path(
    "ontology/rule_registry.json"
)

registry = json.loads(
    RULES_FILE.read_text()
)

print()
print("=" * 60)
print("RULE REGISTRY REPORT")
print("=" * 60)

print()
print(
    "TYPE:",
    type(registry)
)

print()

if isinstance(registry, dict):

    print(
        "Total Keys:",
        len(registry)
    )

    print()

    for k, v in list(registry.items())[:50]:

        print()
        print("KEY:", k)
        print("VALUE:", v)

elif isinstance(registry, list):

    print(
        "Total Items:",
        len(registry)
    )

    for item in registry[:50]:

        print(item)