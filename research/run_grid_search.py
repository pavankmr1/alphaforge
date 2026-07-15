import argparse

from experiments.grid_search import GridSearch


def main():

    parser = argparse.ArgumentParser(

        description="AlphaForge Grid Search"

    )

    parser.add_argument(

        "--strategy",

        required=True

    )

    parser.add_argument(

        "--symbol",

        required=True

    )

    parser.add_argument(

        "--start",

        required=True

    )

    parser.add_argument(

        "--end",

        required=True

    )

    args = parser.parse_args()

    # =====================================================
    # Parameter Space
    # =====================================================

    parameter_space = {

        "min_gap_atr": [

            0.3,

            0.5,

            0.7

        ],

        "stop_buffer": [

            0.0,

            0.25,

            0.5

        ],

        "require_trend": [

            True,

            False

        ]

    }

    # =====================================================
    # Run Grid Search
    # =====================================================

    grid = GridSearch()

    df = grid.run(

        strategy=args.strategy,

        symbol=args.symbol,

        start=args.start,

        end=args.end,

        parameter_space=parameter_space

    )

    print()

    print("=" * 80)

    print("GRID SEARCH RESULTS")

    print("=" * 80)

    print()

    print(df)

    print()

    output = "experiments/grid_search_results.csv"

    df.to_csv(

        output,

        index=False

    )

    print(

        f"Saved results to {output}"

    )


if __name__ == "__main__":

    main()