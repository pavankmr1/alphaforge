# ==========================================
# FIELD NORMALIZATION MAP
# ==========================================
NORMALIZATION_MAP = {

    # --------------------------
    # Generic Price References
    # --------------------------
    "Price": "Close",
    "Market": "Close",
    "Chart": "Close",

    # --------------------------
    # Trend References
    # --------------------------
    "Trend": "EMA20",
    "Downtrend": "EMA20",
    "Uptrend": "EMA20",
    "OverallTrend": "EMA20",
    "TrendFilter": "EMA20",
    "HigherTimeframeTrend": "EMA200",
    "HTF Trend": "EMA200",

    # --------------------------
    # EMA References
    # --------------------------
    "EMA": "EMA20",
    "EMA Support": "EMA20",
    "EMA Support Zone": "EMA20",
    "EMA Resistance Area": "EMA20",

    # --------------------------
    # Volume References
    # --------------------------
    "AverageVolume": "VOL_MA20",
    "SMA20Volume": "VOL_MA20",

    # --------------------------
    # Support / Resistance
    # --------------------------
    "SupportZone": "Support",
    "ResistanceZone": "Resistance",

    "StrongSupport": "Support",
    "StrongResistance": "Resistance",

    "Level": "Resistance",
    "HorizontalLevel": "Resistance",

    "BreakoutLevel": "PreviousHigh",

    # --------------------------
    # Timeframe References
    # --------------------------
    "Daily": None,
    "Weekly": None,
    "4H": None,
    "1H": None,
    "30M": None,
    "15m": None,
    "5m": None,
    "1m": None,

    "Time": None,
    "Timeframe": None,

    # --------------------------
    # Session References
    # --------------------------
    "Session": None,
    "SessionAsia": None,
    "SessionLondon": None,
    "SessionNewYork": None,
    "London": None,
    "NewYork": None,

    # --------------------------
    # Wick References
    # --------------------------
    "UpperWick": "High",
    "LowerWick": "Low",

    # --------------------------
    # Swing References
    # --------------------------
    "SwingHigh": "PreviousHigh",
    "SwingLow": "PreviousLow",

    "SwingHighs": "PreviousHigh",
    "SwingLows": "PreviousLow",

    "PreviousSwingHigh": "PreviousHigh",
    "PreviousSwingLow": "PreviousLow",

    # --------------------------
    # Day References
    # --------------------------
    "PrevDayLow": "PreviousDayLow",
    "PreviousDayLow": "PreviousDayLow",

    "PreviousDayHigh": "PreviousDayHigh",

    # --------------------------
    # Opening Range
    # --------------------------
    "OpenRangeHigh": "PreviousHigh",
    "OpeningRangeHigh": "PreviousHigh",

    "OpenRangeLow": "PreviousLow",
    "OpeningRangeLow": "PreviousLow",

    # --------------------------
    # Market Structure
    # --------------------------
    "Structure": "EMA200",
    "MarketStructure": "EMA200",

    # --------------------------
    # RSI Variants
    # --------------------------
    "StochasticRSI": "RSI14",
    "Stochastic RSI": "RSI14",

    # --------------------------
    # Moving Averages
    # --------------------------
    "SMA200": "EMA200",
    "SMA18": "EMA20",

    # --------------------------
    # Misc
    # --------------------------
    "Confirmation": None,
    "Setup": None,
    "Input": None,
    "Unknown": None,
    "Required": None,
    "N/A": None
}


# ==========================================
# NORMALIZE FIELD
# ==========================================
def normalize_field(field):

    if field is None:
        return None

    return NORMALIZATION_MAP.get(
        field,
        field
    )


# ==========================================
# NORMALIZE RULE
# ==========================================
def normalize_rule(rule):

    rule["left"] = normalize_field(
        rule.get("left")
    )

    rule["right"] = normalize_field(
        rule.get("right")
    )

    return rule


# ==========================================
# NORMALIZE DSL
# ==========================================
def normalize_dsl(dsl):

    if not dsl:
        return dsl

    rules = dsl.get(
        "rules",
        []
    )

    normalized_rules = []

    for rule in rules:

        normalized_rules.append(
            normalize_rule(rule)
        )

    dsl["rules"] = normalized_rules

    return dsl