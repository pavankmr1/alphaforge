from pathlib import Path
import json

# ==========================================
# PATHS
# ==========================================
COMPILED_DIR = Path(
    "data/compiled_strategies_v2"
)

# ==========================================
# HELPERS
# ==========================================
def rule_key(rule):

    return (
        rule.get("left"),
        rule.get("right")
    )


# ==========================================
# SCAN STRATEGIES
# ==========================================
total_contradictions = 0

for file in COMPILED_DIR.glob("*.json"):

    strategy = json.loads(
        file.read_text()
    )

    contradictions = []

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

        # ----------------------------------
        # Compare every rule pair
        # ----------------------------------
        for i in range(len(rules)):

            r1 = rules[i]

            for j in range(i + 1, len(rules)):

                r2 = rules[j]

                # ==========================
                # trend_up vs trend_down
                # ==========================
                if (
                    r1["type"] == "trend_up"
                    and
                    r2["type"] == "trend_down"
                    and
                    r1["left"] == r2["left"]
                ):

                    contradictions.append(
                        (
                            r1,
                            r2,
                            "trend contradiction"
                        )
                    )

                # ==========================
                # cross_above vs cross_below
                # ==========================
                if (
                    r1["type"] == "cross_above"
                    and
                    r2["type"] == "cross_below"
                    and
                    rule_key(r1)
                    ==
                    rule_key(r2)
                ):

                    contradictions.append(
                        (
                            r1,
                            r2,
                            "cross contradiction"
                        )
                    )

                # ==========================
                # price_above vs price_below
                # ==========================
                if (
                    r1["type"] == "price_above"
                    and
                    r2["type"] == "price_below"
                    and
                    r1["right"] == r2["right"]
                ):

                    contradictions.append(
                        (
                            r1,
                            r2,
                            "price contradiction"
                        )
                    )

    # ======================================
    # PRINT
    # ======================================
    if contradictions:

        total_contradictions += len(
            contradictions
        )

        print("\n")
        print("=" * 60)
        print(file.name)
        print("=" * 60)

        for c in contradictions:

            print(
                f"\n[{c[2]}]"
            )

            print(
                c[0]
            )

            print(
                c[1]
            )

print("\n")
print("=" * 60)
print(
    f"Total Contradictions: "
    f"{total_contradictions}"
)
print("=" * 60)