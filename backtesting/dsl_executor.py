from loguru import logger
import pandas as pd

def execute_rule(
    rule,
    data
):
    if (
        rule.get("left") is None
        and rule.get("right") is None
    ):
        return pd.Series(
            True,
            index=data.index
        )

    rule_type = rule.get(
        "type"
    )

    try:

        # ==========================
        # CROSS ABOVE
        # ==========================
        if rule_type == "cross_above":

            left = rule["left"]
            right = rule["right"]

            return (

                (data[left] > data[right])

                &

                (
                    data[left].shift(1)
                    <=
                    data[right].shift(1)
                )
            )

        # ==========================
        # CROSS BELOW
        # ==========================
        elif rule_type == "cross_below":

            left = rule["left"]
            right = rule["right"]

            return (

                (data[left] < data[right])

                &

                (
                    data[left].shift(1)
                    >=
                    data[right].shift(1)
                )
            )

        # ==========================
        # GREATER THAN
        # ==========================
        elif rule_type == "greater_than":

            left = rule.get("left")
            right = rule.get("right")
            value = rule.get("value")

            # Metadata rules
            if left in [
                "Time",
                "Timeframe",
                "Session",
                "HTF",
                "LTF"
            ]:

                return pd.Series(
                    True,
                    index=data.index
                )

            # Numeric comparison
            if value is not None:

                return (
                    data[left]
                    > value
                )

            # Column comparison
            if right in data.columns:

                return (
                    data[left]
                    > data[right]
                )

            return pd.Series(
                True,
                index=data.index
            )

        # ==========================
        # LESS THAN
        # ==========================
        elif rule_type == "less_than":

            left = rule.get("left")
            right = rule.get("right")
            value = rule.get("value")

            if value is not None:

                return (
                    data[left]
                    < value
                )

            if right in data.columns:

                return (
                    data[left]
                    < data[right]
                )

            return pd.Series(
                True,
                index=data.index
            )
        # ==========================
        # PRICE ABOVE
        # ==========================
        elif rule_type == "price_above":

            return (

                data["Close"]
                >
                data[rule["right"]]
            )

        # ==========================
        # PRICE BELOW
        # ==========================
        elif rule_type == "price_below":

            return (

                data["Close"]
                <
                data[rule["right"]]
            )

        # ==========================
        # TREND UP
        # ==========================
        elif rule_type == "trend_up":

            return (

                data[rule["left"]]
                >
                data[rule["left"]].shift(1)
            )

        # ==========================
        # TREND DOWN
        # ==========================
        elif rule_type == "trend_down":

            return (

                data[rule["left"]]
                <
                data[rule["left"]].shift(1)
            )

        # ==========================
        # VOLUME ABOVE
        # ==========================
        elif rule_type == "volume_above":

            return (

                data["Volume"]
                >
                data["VOL_MA20"]
            )
        
       
        logger.warning(
            f"Unknown DSL type: {rule_type}"
        )

        return None

    except Exception as e:

        logger.error(
            f"Failed executing DSL rule: {rule}"
        )

        logger.error(str(e))

        return pd.Series(
            True,
            index=data.index
        )