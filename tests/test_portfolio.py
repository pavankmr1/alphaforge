# from paper_trading.execution_engine import ExecutionEngine
from paper_trading.paper_broker import PaperBroker
from paper_trading.portfolio import Portfolio
# from paper_trading.position_manager import PositionManager
# from paper_trading.risk_manager import RiskManager
from paper_trading.trade_journal import TradeJournal


def test_empty_portfolio():

    broker = PaperBroker()
    journal = TradeJournal()

    # portfolio = Portfolio(
    #     broker,
    #     broker.position_manager,
    #     journal
    # )
    portfolio = Portfolio(
        broker,
        journal
    )
    assert portfolio.cash() == broker.available_cash()
    assert portfolio.market_value() == 0.0
    assert portfolio.total_value() == broker.available_cash()
    assert portfolio.realized_pnl() == 0.0
    assert portfolio.unrealized_pnl() == 0.0
    assert portfolio.open_positions() == 0

def test_market_value():

    broker = PaperBroker()

    broker.buy(
        price=100,
        quantity=10
    )

    broker.position_manager.update_price(120)

    # portfolio = Portfolio(
    #     broker,
    #     broker.position_manager,
    #     TradeJournal()
    # )
    journal = TradeJournal()

    portfolio = Portfolio(
        broker,
        journal
    )

    assert portfolio.market_value() == 1200.0

def test_total_value():

    broker = PaperBroker()

    broker.buy(
        price=100,
        quantity=10
    )

    broker.position_manager.update_price(120)

    # portfolio = Portfolio(
    #     broker,
    #     broker.position_manager,
    #     TradeJournal()
    # )
    journal = TradeJournal()

    portfolio = Portfolio(
        broker,
        journal
    )
    expected = (
        broker.available_cash()
        + 1200.0
    )

    assert portfolio.total_value() == expected
def test_unrealized_pnl():

    broker = PaperBroker()

    broker.buy(
        price=100,
        quantity=10
    )

    broker.position_manager.update_price(130)

    # portfolio = Portfolio(
    #     broker,
    #     broker.position_manager,
    #     TradeJournal()
    # )
    journal = TradeJournal()

    portfolio = Portfolio(
        broker,
        journal
    )

    assert portfolio.unrealized_pnl() == 300.0

def test_summary():

    broker = PaperBroker()

    # portfolio = Portfolio(
    #     broker,
    #     broker.position_manager,
    #     TradeJournal()
    # )

    journal = TradeJournal()

    portfolio = Portfolio(
        broker,
        journal
    )

    summary = portfolio.summary()

    assert "cash" in summary
    assert "market_value" in summary
    assert "total_value" in summary
    assert "realized_pnl" in summary
    assert "unrealized_pnl" in summary
    assert "open_positions" in summary