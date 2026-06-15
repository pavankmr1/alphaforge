from copy import deepcopy

# ==========================================
# COMMON ALIASES
# ==========================================
NORMALIZATION_MAP = {

    # price aliases

    "Price":
        "Close",

    "Market":
        "Close",

    "Trend":
        "Close",

    # EMA aliases

    "EMA":
        "EMA20",

    "EMA Support":
        "EMA20",

    "EMA Resistance Area":
        "EMA20",

    "EMA Support Zone":
        "EMA20",

    # RSI aliases

    "RSI":
        "RSI14",

    # volume aliases

    "AverageVolume":
        "VOL_MA20"
}


# ==========================================
# NORMALIZE RULE
# ==========================================
def normalize_rule(rule):

    rule = deepcopy(rule)

    left = rule.get(
        "left"
    )

    right = rule.get(
        "right"
    )

    if left in NORMALIZATION_MAP:

        rule["left"] = (
            NORMALIZATION_MAP[left]
        )

    if right in NORMALIZATION_MAP:

        rule["right"] = (
            NORMALIZATION_MAP[right]
        )

    return rule


# ==========================================
# NORMALIZE DSL
# ==========================================
def normalize_dsl(dsl):

    rules = dsl.get(
        "rules",
        []
    )

    normalized_rules = []

    for rule in rules:

        normalized_rules.append(

            normalize_rule(
                rule
            )
        )

    dsl["rules"] = (
        normalized_rules
    )

    return dsl