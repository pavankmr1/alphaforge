
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


def test_gross_profit():

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
            exit_price=90,
            pnl=-50,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.gross_profit() == 300

def test_gross_loss():

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

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=80,
            pnl=-50,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.gross_loss() == 150

def test_net_pnl():

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
            exit_price=90,
            pnl=-50,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.net_pnl() == 150

def test_win_rate():

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
            exit_price=90,
            pnl=-100,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    assert analytics.win_rate() == 50.0

def test_average_win():

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
            pnl=300,
        )
    )

    analytics = PerformanceAnalytics(portfolio, journal)

    assert analytics.average_win() == 200

def test_average_loss():

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

    journal.record(
        TradeRecord(
            strategy="EMA",
            symbol="NIFTY",
            side="BUY",
            quantity=1,
            entry_time=None,
            exit_time=None,
            entry_price=100,
            exit_price=80,
            pnl=-300,
        )
    )

    analytics = PerformanceAnalytics(portfolio, journal)

    assert analytics.average_loss() == 200

def test_profit_factor():

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
            exit_price=120,
            pnl=400,
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
            exit_price=90,
            pnl=-200,
        )
    )

    analytics = PerformanceAnalytics(portfolio, journal)

    assert analytics.profit_factor() == 2.0

def test_expectancy():

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
            exit_price=120,
            pnl=300,
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
            exit_price=90,
            pnl=-100,
        )
    )

    analytics = PerformanceAnalytics(portfolio, journal)

    assert analytics.expectancy() == 100

def test_summary():

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
            exit_price=120,
            pnl=300,
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
            exit_price=90,
            pnl=-100,
        )
    )

    analytics = PerformanceAnalytics(
        portfolio,
        journal,
    )

    summary = analytics.summary()

    assert summary["total_trades"] == 2
    assert summary["winning_trades"] == 1
    assert summary["losing_trades"] == 1

    assert summary["gross_profit"] == 300
    assert summary["gross_loss"] == 100
    assert summary["net_pnl"] == 200

    assert summary["win_rate"] == 50.0

    assert summary["average_win"] == 300
    assert summary["average_loss"] == 100

    assert summary["profit_factor"] == 3.0
    assert summary["expectancy"] == 100