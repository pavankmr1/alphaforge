from collections import Counter


class UnicornValidator:

    def __init__(self, strategy):

        self.strategy = strategy

        self.events = strategy.context.event_log

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        print("\n" + "=" * 80)
        print("UNICORN VALIDATOR")
        print("=" * 80)

        counts = Counter(
            e["event"]
            for e in self.events
        )

        print()

        for event, count in sorted(counts.items()):

            print(f"{event:<25} {count}")

        print()

        print("=" * 80)

    # =====================================================
    # EVENT TIMELINE
    # =====================================================

    def timeline(self):

        print("\nEVENT TIMELINE\n")

        for e in self.events:

            print(
                f"{e['time']}   {e['event']}"
            )

    # =====================================================
    # CHECK ORDER
    # =====================================================

    def validate_order(self):

        expected = [

            "SWEEP",

            "MSS",

            "HTF_FVG",

            "LTF_FVG",

            "RETEST",

            "ENTRY"

        ]

        print("\nORDER VALIDATION\n")

        trade = []

        trade_no = 1

        for e in self.events:

            trade.append(
                e["event"]
            )

            if e["event"] == "ENTRY":

                print(
                    f"Trade {trade_no}"
                )

                print(
                    " -> ".join(trade)
                )

                ok = True

                idx = 0

                for x in trade:

                    if idx < len(expected) and x == expected[idx]:

                        idx += 1

                if idx == len(expected):

                    print("PASS\n")

                else:

                    print("FAIL\n")

                trade = []

                trade_no += 1

    # =====================================================
    # BROKEN FVGS
    # =====================================================

    def broken_fvgs(self):

        print("\nBROKEN FVG\n")

        for e in self.events:

            if e["event"] == "FVG_INVALIDATED":

                print(
                    e["time"],
                    e["details"]
                )

    # =====================================================
    # ENTRIES
    # =====================================================

    def entries(self):

        print("\nENTRIES\n")

        for e in self.events:

            if e["event"] == "ENTRY":

                print(
                    e["time"],
                    e["details"]
                )

    # =====================================================
    # FULL REPORT
    # =====================================================

    def report(self):

        self.summary()

        self.validate_order()

        self.broken_fvgs()

        self.entries()