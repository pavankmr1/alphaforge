RULE_MAPPINGS = {

    "strong bullish candle": {
        "logic_type": "momentum",
        "formula":
        "(close - open) > ATR * 0.4"
    },

    "strong bearish candle": {
        "logic_type": "momentum",
        "formula":
        "(open - close) > ATR * 0.4"
    },

    "liquidity sweep high": {
        "logic_type": "liquidity",
        "formula":
        "high > ta.highest(high[1], 5)"
    },

    "liquidity sweep low": {
        "logic_type": "liquidity",
        "formula":
        "low < ta.lowest(low[1], 5)"
    },

    "bullish displacement": {
        "logic_type": "displacement",
        "formula":
        "close > high[1]"
    },

    "bearish displacement": {
        "logic_type": "displacement",
        "formula":
        "close < low[1]"
    }
}