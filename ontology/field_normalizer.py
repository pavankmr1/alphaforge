# ==========================================
# FIELD NORMALIZATION MAP
# ==========================================
NORMALIZATION_MAP = {
    "Candle1.Midpoint": "Pivot",
    "Midpoint": "Pivot",

    "FirstCandleLow": "PreviousLow",
    "SetupCandleLow": "PreviousLow",
    "ConfirmationCandleLow": "PreviousLow",

    "SetupCandleHigh": "PreviousHigh",

    "TradeDirection": "EMA200",
    "15m Market Trend": "EMA200",

    "5m Resistance": "Resistance",

    "Volatility": "ATR14",
    "Threshold": "ATR14",

    "PreviousCandleRange": "ATR14",

    "DominantTrend": "EMA200",

    "PreviousClose": "PreviousClose",

    "BreakoutHigh": "PreviousHigh",

    "StrongBullishUptrend": "EMA200",

    "SidewaysRange": "ATR14",
    "Momentum": "ATR14",
    "Bullish": "EMA20",
    "Bearish": "EMA20",

    "Bias": "EMA200",
    "Market trend": "EMA200",

    "Range": "ATR14",

    "Confirmation Candle": "Close",
    "ConfirmationCandle": "Close",

    "BearishTrendline": "EMA20",

    "HTF Market Structure": "EMA200",

    "POI": "Support",

    "OrderBlockLower": "Support",

    "BreakoutStrength": "ATR14",

    "Touch": "PreviousHigh",

    "Confirmation Candle High": "High",

    "Next Candle High": "High",

    "First 5-minute candle high": "PreviousHigh",

    "Close[3]": "Close",
    "High[1]": "High",

    "Candle3.Low": "Low",

    "Midpoint(Candle1.Range)": "Pivot",

    "Buy": None,
    "Sell": None,

    "Long": None,
    # --------------------------
    # Generic Price References
    # --------------------------
    "Price": "Close",
    "Market": "Close",
    "Chart": "Close",
    # --------------------------
    # Trendlines
    # --------------------------
    "Trendline": "EMA20",
    "BullishTrendline": "EMA20",

    # --------------------------
    # Order Blocks / Liquidity
    # --------------------------
    "OrderBlock": "Support",
    "Liquidity": "LiquidityHigh",
    "Zone": "Support",

    # --------------------------
    # Breakout Concepts
    # --------------------------
    "Breakout": "PreviousHigh",
    "BreakoutConfirmation": "PreviousHigh",

    # --------------------------
    # Market Profile
    # --------------------------
    "MarketProfile": "VWAP",

    # --------------------------
    # Direction
    # --------------------------
    "Up": "EMA20",
    "Down": "EMA20",

    # --------------------------
    # Candle References
    # --------------------------
    "Candle": "Close",
    "Candle3.Close": "Close",
    "Candle1.Low": "Low",

    "ConfirmationCandleHigh": "High",
    "Confirmation Candle Low": "Low",

    "BullishConfirmationCandleHigh": "High",

    "MomentumCandle": "Close",

    "High2": "High",

    # --------------------------
    # Previous Candle
    # --------------------------
    "PrevCandleRange": "ATR14",

    # --------------------------
    # First 5 Minute
    # --------------------------
    "First5MinHigh": "PreviousHigh",
    "First5MinLow": "PreviousLow",

    "First 5-minute candle low": "PreviousLow",
    "Second 5-minute candle low": "PreviousLow",

    # --------------------------
    # Higher Timeframe
    # --------------------------
    "HigherTimeframe": "EMA200",
    "ConfirmOn5mOr15m": None,
    "ChartTimeframe": None,

    # --------------------------
    # Time Values
    # --------------------------
    "09:30": None,
    "19:00 IST": None,

    # --------------------------
    # Numeric Garbage
    # --------------------------
    "0": None,
    "1": None,
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
    "N/A": None,
    "Valuation": None,
    "HistoricalAverage": None,
    "Purchases": None,
    "Equities": None,

    "Fundamentals": None,
    "CashFlow": None,
    "Positive": None,
    "Earnings": None,
    "Sustainable": None,
    "Attractive": None,
    "DividendYield": None,

    "LongTermPlan": None,
    "AssetAllocation": None,
    "LongTermWealthCreation": None,
    "Inflation": None,

    "TradesPerDay": None,
    "CrossoverAngle": None,
    "EntryLong": None,
    "Pattern": None,
    "Strong": None,
    "BuyConfirmation": None,
    "SellSetup": None,

    "ConfirmationCandlesOrStrongPriceAction": None,

    "NotChoppy": None,

    "TradeCount": None,

    "FirstRetest": None,

    "ContinuationConfirmation": None,

    "ReversalMomentum": None,
    "SpeculativeBuying": None,

    "HistoricalAverageValuation": None,
    "HistoricalAverageDividendYield": None,

    "LongTermInvestmentPlan": None,
    "SelectedAssetAllocation": None,

    "Rumors": None,
    "Tips": None,

    "NewsImpact": None,
    "5m Close": "Close",

    "FibonacciPivot": "Pivot",
    "PivotLevel": "Pivot",

    "PreviousClose": "PreviousClose",

    "PrevCandleHigh": "PreviousHigh",

    "Resistance5m": "Resistance",

    "FastEMA": "EMA9",
    "SlowEMA": "EMA20",

    "BreakoutDirection": "EMA200",

    "PriceConfirmation": "Close",

    "Confirmed": None,

    "Confirmation/Rejection": None,
    "ConfirmationCandles": None,
    "StrongPriceAction": None,

    "MaxTrades": None,

    "ShortSetup": None,
    "LongSetup": None,

    "NotSideways": "ATR14",

    "SwingPoints": "PreviousHigh",
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