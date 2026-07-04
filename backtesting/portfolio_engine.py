
from statistics import mean


class PortfolioEngine:

    """
    Calculates performance statistics from completed trades.
    """

    def __init__(self, trades):

        self.trades = trades
    def total_trades(self):

        return len(self.trades)
    def winners(self):

        return [

            t

            for t in self.trades

            if t.pnl > 0

        ]
    def losers(self):

        return [

            t

            for t in self.trades

            if t.pnl <= 0

        ]
    def win_rate(self):

        if not self.trades:

            return 0

        return (

            len(self.winners())

            /

            len(self.trades)

        )
    def total_pnl(self):

        return sum(

            t.pnl

            for t in self.trades

        )
    def average_winner(self):

        wins = self.winners()

        if not wins:

            return 0

        return mean(

            t.pnl

            for t in wins

        )
    def average_loser(self):

        losses = self.losers()

        if not losses:

            return 0

        return mean(

            t.pnl

            for t in losses

        )
    def profit_factor(self):

        gross_profit = sum(

            t.pnl

            for t in self.winners()

        )

        gross_loss = abs(

            sum(

                t.pnl

                for t in self.losers()

            )

        )

        if gross_loss == 0:

            return float("inf")

        return gross_profit / gross_loss
    def average_rr(self):

        if not self.trades:

            return 0

        return mean(

            t.rr

            for t in self.trades

        )
    def best_trade(self):

        if not self.trades:

            return None

        return max(

            self.trades,

            key=lambda x: x.pnl

        )
    def worst_trade(self):

        if not self.trades:

            return None

        return min(

            self.trades,

            key=lambda x: x.pnl

        )
    def summary(self):

        print()

        print("=" * 80)

        print("PORTFOLIO REPORT")

        print("=" * 80)

        print()

        print("Trades :", self.total_trades())

        print("Wins :", len(self.winners()))

        print("Losses :", len(self.losers()))

        print()

        print("Win Rate :", round(self.win_rate() * 100, 2), "%")

        print("Profit Factor :", round(self.profit_factor(), 2))

        print("Average RR :", round(self.average_rr(), 2))

        print()

        print("Total PnL :", round(self.total_pnl(), 2))

        print("Average Winner :", round(self.average_winner(), 2))

        print("Average Loser :", round(self.average_loser(), 2))

        print()

        best = self.best_trade()

        worst = self.worst_trade()

        if best:

            print("Best Trade :", round(best.pnl, 2))

        if worst:

            print("Worst Trade :", round(worst.pnl, 2))