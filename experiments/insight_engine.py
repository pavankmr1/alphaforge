from openai import OpenAI
from dotenv import load_dotenv

import os

# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

# ==========================================
# GENERATE INSIGHT
# ==========================================
def generate_insight(
    strategy_name,
    metrics
):

    prompt = f"""
You are an elite quantitative
trading research analyst.

Analyze these backtest metrics
and provide:

1. Strengths
2. Weaknesses
3. Risk observations
4. Improvement suggestions

Strategy:
{strategy_name}

Metrics:
{metrics}
"""

    response = (
        client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are a professional quant analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    )

    return (
        response
        .choices[0]
        .message.content
    )