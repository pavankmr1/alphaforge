from loguru import logger

# ==========================================
# VALID FEATURE REGISTRY
# ==========================================

VALID_FIELDS = {

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "EMA5",
    "EMA9",
    "EMA10",
    "EMA15",
    "EMA20",
    "EMA21",
    "EMA50",
    "EMA200",

    "VWAP",
    "ATR14",
    "RSI14",

    "VOL_MA20",

    "Support",
    "Resistance",

    "PreviousHigh",
    "PreviousLow",

    "PreviousDayHigh",
    "PreviousDayLow",

    "Pivot"
}


# ==========================================
# VALIDATE SINGLE RULE
# ==========================================

def validate_rule(rule):

    left = rule.get("left")
    right = rule.get("right")

    rule["validation_status"] = "valid"

    if left:

        if (
            isinstance(left, str)
            and
            left not in VALID_FIELDS
        ):

            rule["validation_status"] = "invalid"

            logger.warning(
                f"Invalid LEFT field: {left}"
            )

    if right:

        if (
            isinstance(right, str)
            and
            right not in VALID_FIELDS
        ):

            rule["validation_status"] = "invalid"

            logger.warning(
                f"Invalid RIGHT field: {right}"
            )

    return rule


# ==========================================
# VALIDATE DSL BLOCK
# ==========================================

def validate_dsl(dsl):

    rules = dsl.get(
        "rules",
        []
    )

    validated_rules = []

    for rule in rules:

        validated_rules.append(
            validate_rule(rule)
        )

    dsl["rules"] = validated_rules

    return dsl