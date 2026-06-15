from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from openai import OpenAI
import instructor

import json
import os
from ontology.dsl_normalizer import (
    normalize_dsl
)
from schemas.dsl_schema import (
    DSLResponse
)

# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

# ==========================================
# OPENAI CLIENT
# ==========================================
client = instructor.from_openai(
    OpenAI(
        api_key=OPENAI_API_KEY
    )
)

# ==========================================
# COMPILE CONDITION
# ==========================================
def compile_condition(
    condition: str
):

    logger.info(
        f"Compiling condition: "
        f"{condition}"
    )

    response = client.chat.completions.create(

        model="gpt-5.4-mini",

        response_model=DSLResponse,

        messages=[

            {
                "role": "system",

                "content": """
You are AlphaForge DSL Compiler.

Convert trading conditions into structured DSL.

Supported DSL types:

cross_above
cross_below

greater_than
less_than

trend_up
trend_down

price_above
price_below

volume_above

Examples:

9 EMA crosses above 20 EMA

->

{
    "rules": [
        {
            "type":"cross_above",
            "left":"EMA9",
            "right":"EMA20"
        }
    ]
}

Price above VWAP

->

{
    "rules": [
        {
            "type":"price_above",
            "left":"Close",
            "right":"VWAP"
        }
    ]
}

Return ONLY valid DSL.
"""
            },

            {
                "role": "user",

                "content": condition
            }
        ]
    )

    dsl = response.model_dump()

    dsl = normalize_dsl(
        dsl
    )

    return DSLResponse(
        **dsl
    )