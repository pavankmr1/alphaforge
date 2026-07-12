import math


class ResearchScore:

    """
    Computes a composite research score for an experiment.

    Higher is better.
    """

    @staticmethod
    def score(metrics):

        pf = max(0.0, metrics.get("profit_factor") or 0.0)
        win_rate = max(0.0, metrics.get("win_rate") or 0.0)
        rr = max(0.0, metrics.get("average_rr") or 0.0)
        pnl = max(0.0, metrics.get("total_pnl") or 0.0)
        trades = max(0, metrics.get("total_trades") or 0)

        # Normalization

        pf_score = min(pf / 3.0, 1.0)

        rr_score = min(rr / 3.0, 1.0)

        pnl_score = min(
            math.log1p(pnl) / 10.0,
            1.0
        )

        trade_score = min(
            trades / 100.0,
            1.0
        )

        score = (

            0.40 * pf_score +

            0.20 * win_rate +

            0.15 * rr_score +

            0.15 * pnl_score +

            0.10 * trade_score

        )

        return round(score * 100, 2)