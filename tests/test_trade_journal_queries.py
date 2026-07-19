from paper_trading.trade_journal import (
    TradeJournal,
    TradeRecord,
)

def test_empty_journal():

    journal = TradeJournal()

    assert journal.is_empty()

    assert journal.all_trades() == []

    assert journal.winning_trades() == []

    assert journal.losing_trades() == []


def test_winning_trade():

    journal = TradeJournal()

    trade = TradeRecord(
        strategy="EMA",
        symbol="NIFTY",
        side="BUY",
        quantity=10,
        entry_time=None,
        exit_time=None,
        entry_price=100,
        exit_price=110,
        pnl=100,
    )

    journal.record(trade)

    assert len(journal.winning_trades()) == 1

    assert len(journal.losing_trades()) == 0

def test_losing_trade():

    journal = TradeJournal()

    trade = TradeRecord(
        strategy="EMA",
        symbol="NIFTY",
        side="BUY",
        quantity=10,
        entry_time=None,
        exit_time=None,
        entry_price=100,
        exit_price=90,
        pnl=-100,
    )

    journal.record(trade)

    assert len(journal.winning_trades()) == 0

    assert len(journal.losing_trades()) == 1

def test_mixed_trades():

    journal = TradeJournal()

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

    assert len(journal.all_trades()) == 2

    assert len(journal.winning_trades()) == 1

    assert len(journal.losing_trades()) == 1