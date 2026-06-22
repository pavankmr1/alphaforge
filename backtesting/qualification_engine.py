import pandas as pd

def qualify_bullish_setup(
    setup,
    bullish_context,
    bullish_structure
):

    qualified = (

        setup

        &

        bullish_context

        &

        bullish_structure

    )

    return qualified.fillna(False)
# def qualify_bullish_setup(

#     setup,
#     bullish_context,
#     bullish_structure

# ):

#     qualified = (

#         setup

#         &

#         (
#             bullish_context
#             |
#             bullish_structure
#         )

#     )

#     return qualified.fillna(False)