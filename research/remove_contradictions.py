from pathlib import Path
import json

# ==========================================
# PATHS
# ==========================================
INPUT_DIR = Path(
    "data/compiled_strategies_v2"
)

OUTPUT_DIR = Path(
    "data/compiled_strategies_v3"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

removed_count = 0


# ==========================================
# HELPERS
# ==========================================
def is_contradiction(
    rule1,
    rule2
):

    # --------------------------
    # trend_up vs trend_down
    # --------------------------
    if (
        rule1["type"] == "trend_up"
        and
        rule2["type"] == "trend_down"
        and
        rule1.get("left")
        ==
        rule2.get("left")
    ):
        return True

    # --------------------------
    # cross_above vs cross_below
    # --------------------------
    if (
        rule1["type"] == "cross_above"
        and
        rule2["type"] == "cross_below"
        and
        rule1.get("left")
        ==
        rule2.get("left")
        and
        rule1.get("right")
        ==
        rule2.get("right")
    ):
        return True

    # --------------------------
    # price_above vs price_below
    # --------------------------
    if (
        rule1["type"] == "price_above"
        and
        rule2["type"] == "price_below"
        and
        rule1.get("right")
        ==
        rule2.get("right")
    ):
        return True

    return False


# ==========================================
# PROCESS STRATEGIES
# ==========================================
files = list(
    INPUT_DIR.glob("*.json")
)

print(
    f"\nFound {len(files)} strategies"
)

for file in files:

    strategy = json.loads(
        file.read_text()
    )

    strategy_removed = 0

    for item in strategy.get(
        "compiled_entry_logic",
        []
    ):

        dsl = item.get("dsl")

        if not dsl:
            continue

        rules = dsl.get(
            "rules",
            []
        )

        keep_rules = []

        skip_indexes = set()

        for i in range(
            len(rules)
        ):

            if i in skip_indexes:
                continue

            rule1 = rules[i]

            contradiction_found = False

            for j in range(
                i + 1,
                len(rules)
            ):

                if j in skip_indexes:
                    continue

                rule2 = rules[j]

                if is_contradiction(
                    rule1,
                    rule2
                ):

                    contradiction_found = True

                    skip_indexes.add(i)
                    skip_indexes.add(j)

                    strategy_removed += 2
                    removed_count += 2

                    print(
                        f"\n[{file.name}]"
                    )

                    print(
                        "REMOVED:"
                    )

                    print(rule1)
                    print(rule2)

                    break

            if not contradiction_found:
                keep_rules.append(
                    rule1
                )

        dsl["rules"] = keep_rules

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
            strategy,
            f,
            indent=4
        )

    print(
        f"\n{file.name}"
        f" -> removed "
        f"{strategy_removed} rules"
    )

print(
    "\n================================"
)

print(
    f"Total Rules Removed: "
    f"{removed_count}"
)

print(
    "================================"
)