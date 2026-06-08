from loguru import logger

from signal_engine import (
    generate_signals
)

# ==========================================
# ADAPT STRATEGY
# ==========================================
def adapt_strategy(
    strategy_data,
    market_data
):

    logger.info(
        "Adapting strategy..."
    )

    compiled_logic = strategy_data.get(
        "compiled_entry_logic",
        []
    )

    signals = generate_signals(
        compiled_logic,
        market_data
    )

    return {

        "strategy_name":
        strategy_data.get("name"),

        "signals":
        signals
    }