NORMALIZATION_MAP = {

    # Price aliases
    "Price": "Close",
    "Market": "Close",

    # Trend aliases
    "Trend": "EMA20",
    "Downtrend": "EMA20",

    # EMA aliases
    "EMA": "EMA20",

    # Volume aliases
    "AverageVolume": "VOL_MA20",

    # Session aliases
    "Time": None,
    "Timeframe": None,

    # Market structure
    "BreakoutLevel": "PreviousHigh",

    # HTF trend
    "HigherTimeframeTrend": "EMA200",

    # Zones
    "SupportZone": "Support",
    "ResistanceZone": "Resistance",

    # Wick logic
    "UpperWick": "High",
    "LowerWick": "Low"
}

def normalize_rule(rule):

    left = rule.get("left")
    right = rule.get("right")

    if left in NORMALIZATION_MAP:
        rule["left"] = NORMALIZATION_MAP[left]

    if right in NORMALIZATION_MAP:
        rule["right"] = NORMALIZATION_MAP[right]

    return rule


def normalize_dsl(dsl):

    rules = dsl.get(
        "rules",
        []
    )

    for rule in rules:

        normalize_rule(rule)

    return dsl