from paper_trading.trade_journal import (
    TradeJournal,
    TradeRecord,
)


def test_record_trade(tmp_path):

    journal = TradeJournal(

        output_path=tmp_path / "journal.csv"

    )

    trade = TradeRecord(

        strategy="UNICORN",

        symbol="NIFTY",

        side="BUY",

        quantity=10,

        entry_time="2025-01-01 09:30",

        exit_time="2025-01-01 10:15",

        entry_price=100,

        exit_price=110,

        pnl=100,

        stop_loss=95,

        target=120

    )

    journal.record(trade)

    assert len(journal) == 1


def test_dataframe(tmp_path):

    journal = TradeJournal(

        output_path=tmp_path / "journal.csv"

    )

    journal.record(

        TradeRecord(

            strategy="UNICORN",

            symbol="NIFTY",

            side="BUY",

            quantity=1,

            entry_time=None,

            exit_time=None,

            entry_price=100,

            exit_price=105,

            pnl=5

        )

    )

    df = journal.dataframe()

    assert len(df) == 1

    assert "pnl" in df.columns


def test_save(tmp_path):

    output = tmp_path / "journal.csv"

    journal = TradeJournal(

        output_path=output

    )

    journal.record(

        TradeRecord(

            strategy="UNICORN",

            symbol="NIFTY",

            side="BUY",

            quantity=1,

            entry_time=None,

            exit_time=None,

            entry_price=100,

            exit_price=105,

            pnl=5

        )

    )

    journal.save()

    assert output.exists()


def test_reset(tmp_path):

    journal = TradeJournal(

        output_path=tmp_path / "journal.csv"

    )

    journal.record(

        TradeRecord(

            strategy="UNICORN",

            symbol="NIFTY",

            side="BUY",

            quantity=1,

            entry_time=None,

            exit_time=None,

            entry_price=100,

            exit_price=101,

            pnl=1

        )

    )

    journal.reset()

    assert len(journal) == 0