from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from openai import OpenAI
import instructor

import json
import os

from pydantic import BaseModel

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
# OUTPUT DIRECTORY
# ==========================================
OUTPUT_DIR = Path(
    "data/ontology_proposals"
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
# SCHEMA
# ==========================================
class OntologyProposal(
    BaseModel
):

    concept: str

    explanation: str

    logic_type: str

    candidate_formula: str

    confidence: float

# ==========================================
# LEARN CONCEPT
# ==========================================
def learn_concept(
    condition_text
):

    logger.info(
        f"Learning concept: "
        f"{condition_text}"
    )

    response = (
        client.chat.completions.create(

            model="gpt-4.1-mini",

            response_model=
            OntologyProposal,

            messages=[

                {
                    "role": "system",
                    "content": """
You are an expert ICT/SMC
quantitative trading ontology engine.

Your job:
- understand trading concepts
- explain them
- propose candidate quant logic
- generate executable-style formulas
- avoid hallucinations
"""
                },

                {
                    "role": "user",
                    "content":
                    condition_text
                }
            ]
        )
    )

    return response

# ==========================================
# SAVE PROPOSAL
# ==========================================
def save_proposal(
    proposal
):

    filename = (
        proposal.concept
        .replace(" ", "_")
        .lower()
    )

    output_file = (
        OUTPUT_DIR /
        f"{filename}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            proposal.model_dump(),
            f,
            indent=4
        )

    logger.success(
        f"Saved ontology proposal: "
        f"{output_file.name}"
    )

# ==========================================
# RUN TEST
# ==========================================
if __name__ == "__main__":

    concept = (
        "strong bullish trend "
        "with consecutive green candles"
    )

    proposal = learn_concept(
        concept
    )

    print(
        proposal.model_dump_json(
            indent=4
        )
    )

    save_proposal(
        proposal
    )