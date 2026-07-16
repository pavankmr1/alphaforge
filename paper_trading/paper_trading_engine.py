from paper_trading.execution_engine import ExecutionEngine
from paper_trading.order_builder import OrderBuilder

class PaperTradingEngine:
    """
    AlphaForge V4

    Coordinates strategy execution
    during paper trading.

    Responsibilities
    ----------------
    - Receive market candles
    - Ask strategy for signals
    - Execute signals
    - Update broker state

    Does NOT

    - Calculate indicators
    - Manage positions
    - Perform risk checks
    """

    def __init__(

        self,

        strategy,

        execution_engine: ExecutionEngine

    ):

        self.strategy = strategy

        self.execution_engine = execution_engine

        self.execution_log = []
        self.order_builder = OrderBuilder()
    # ======================================================
    # PROCESS
    # ======================================================

    def process_candle(

        self,

        candle

    ):

        signal = self.strategy.on_candle(candle)

        order = self.order_builder.build(signal)

        result = self.execution_engine.execute(order)

        self.execution_log.append(result)

        return result

    # ======================================================
    # RUN
    # ======================================================

    def run(

        self,

        candles

    ):

        for candle in candles:

            self.process_candle(candle)

        return self.execution_log

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.execution_log = []