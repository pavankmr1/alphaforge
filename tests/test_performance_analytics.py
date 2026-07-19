
from paper_trading.paper_broker import PaperBroker
from paper_trading.performance_analytics import PerformanceAnalytics
from paper_trading.portfolio import Portfolio
from paper_trading.trade_journal import TradeJournal, TradeRecord
def test_empty_journal():

    broker = PaperBroker()
    journal = TradeJournal()
    portfolio = Portfolio(broker, journal)

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.total_trades() == 0
    assert analytics.winning_trades() == 0
    assert analytics.losing_trades() == 0


def test_one_winning_trade():

    broker = PaperBroker()
    journal = TradeJournal()
    portfolio = Portfolio(broker, journal)

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=110,
            pnl=100,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.total_trades() == 1
    assert analytics.winning_trades() == 1
    assert analytics.losing_trades() == 0

def test_one_losing_trade():

    broker = PaperBroker()
    journal = TradeJournal()
    portfolio = Portfolio(broker, journal)

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=90,
            pnl=-100,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.total_trades() == 1
    assert analytics.winning_trades() == 0
    assert analytics.losing_trades() == 1
def test_mixed_trades():

    broker = PaperBroker()
    journal = TradeJournal()
    portfolio = Portfolio(broker, journal)

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=110,
            pnl=100,
        )
    )

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=120,
            pnl=200,
        )
    )

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=95,
            pnl=-50,
        )
    )

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=75,
            pnl=-75,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.total_trades() == 4
    assert analytics.winning_trades() == 2
    assert analytics.losing_trades() == 2