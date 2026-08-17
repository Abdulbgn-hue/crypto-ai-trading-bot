import os
import json
import requests


AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_URL = os.getenv(
    "AI_API_URL",
    "https://api.openai.com/v1/chat/completions"
)


def build_analysis_prompt(market, technical, research=None):

    research = research or {}

    return f"""
You are a crypto market analysis engine.

Analyze the following data objectively.

MARKET DATA:
{json.dumps(market, indent=2)}

TECHNICAL DATA:
{json.dumps(technical, indent=2)}

PROJECT RESEARCH:
{json.dumps(research, indent=2)}

Return JSON only with:

{{
  "decision": "BUY|WAIT|AVOID",
  "confidence": 0,
  "entry_zone": {{
    "low": null,
    "high": null
  }},
  "stop_loss": null,
  "take_profit": [
    null,
    null,
    null
  ],
  "risk_reward": null,
  "reasons": [],
  "warnings": []
}}

Do not invent missing market data.
If the evidence is insufficient, return WAIT.
"""


def analyze_with_ai(
    market,
    technical,
    research=None,
):

    if not AI_API_KEY:
        return {
            "decision": "WAIT",
            "confidence": 0,
            "entry_zone": {
                "low": None,
                "high": None,
            },
            "stop_loss": None,
            "take_profit": [],
            "risk_reward": None,
            "reasons": [
                "AI API key is not configured."
            ],
            "warnings": [
                "AI analysis is currently disabled."
            ],
        }

    prompt = build_analysis_prompt(
        market,
        technical,
        research,
    )

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": os.getenv(
            "AI_MODEL",
            "gpt-4o-mini"
        ),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful crypto "
                    "market-analysis engine."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.1,
    }

    response = requests.post(
        AI_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    content = (
        data["choices"][0]["message"]["content"]
    )

    return json.loads(content)
