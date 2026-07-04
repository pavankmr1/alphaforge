class StrategyRegistry:

    """
    Central registry of all AlphaForge strategies.
    """

    _strategies = {}

    # ==========================================================
    # REGISTER
    # ==========================================================

    @classmethod
    def register(

        cls,

        name,

        strategy_class

    ):

        cls._strategies[
            name.upper()
        ] = strategy_class

    # ==========================================================
    # CREATE
    # ==========================================================

    @classmethod
    def create(

        cls,

        name,

        *args,

        **kwargs

    ):

        strategy = cls._strategies.get(

            name.upper()

        )

        if strategy is None:

            raise ValueError(

                f"Unknown strategy: {name}"

            )

        return strategy(

            *args,

            **kwargs

        )

    # ==========================================================
    # LIST
    # ==========================================================

    @classmethod
    def available(cls):

        return sorted(

            cls._strategies.keys()

        )