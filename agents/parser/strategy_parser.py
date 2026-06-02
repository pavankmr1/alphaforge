from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from openai import OpenAI
import instructor

import json
import os

from schemas.strategy_schema import StrategySchema

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
    OpenAI(api_key=OPENAI_API_KEY)
)

# ==========================================
# PATHS
# ==========================================
TEXT_DIR = Path(
    "data/extracted_text"
)

OUTPUT_DIR = Path(
    "data/parsed_strategies"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# LOGGING
# ==========================================
logger.add(
    "logs/alphaforge.log",
    rotation="10 MB"
)

# ==========================================
# PARSE STRATEGY
# ==========================================
def parse_strategy(text: str):

    logger.info(
        "Sending strategy to LLM..."
    )

    response = client.chat.completions.create(
        model="gpt-5.4-mini",

        response_model=StrategySchema,

        messages=[
            {
                "role": "system",
                "content": """
You are an expert quantitative trading
strategy extraction engine.

Your job:
- extract trading strategy logic
- structure it deterministically
- avoid hallucinations
- return only structured strategy data
"""
            },

            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response

# ==========================================
# PROCESS TEXT FILES
# ==========================================
def process_text_files():

    txt_files = TEXT_DIR.glob("*.txt")

    for txt_file in txt_files:

        try:

            logger.info(
                f"Processing: {txt_file.name}"
            )

            text = txt_file.read_text(
                encoding="utf-8"
            )

            parsed_strategy = parse_strategy(
                text
            )

            output_file = (
                OUTPUT_DIR /
                f"{txt_file.stem}.json"
            )

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    parsed_strategy.model_dump(),
                    f,
                    indent=4
                )

            logger.success(
                f"Saved parsed strategy: "
                f"{output_file.name}"
            )

        except Exception as e:

            logger.error(
                f"Failed parsing "
                f"{txt_file.name}: {e}"
            )

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":

    process_text_files()