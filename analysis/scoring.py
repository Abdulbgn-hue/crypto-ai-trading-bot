from typing import Dict


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(value, maximum))


def calculate_final_score(
    market_score: float,
    technical_score: float,
    ai_confidence: float,
    research_score: float = 50,
    risk_score: float = 50,
) -> Dict:

    # Weighted score
    final_score = (
        market_score * 0.25
        + technical_score * 0.25
        + ai_confidence * 0.25
        + research_score * 0.15
        + risk_score * 0.10
    )

    final_score = clamp(final_score)

    if final_score >= 80:
        decision = "STRONG_SETUP"
    elif final_score >= 70:
        decision = "SETUP"
    elif final_score >= 55:
        decision = "WATCH"
    else:
        decision = "AVOID"

    return {
        "market_score": round(market_score, 2),
        "technical_score": round(technical_score, 2),
        "ai_confidence": round(ai_confidence, 2),
        "research_score": round(research_score, 2),
        "risk_score": round(risk_score, 2),
        "final_score": round(final_score, 2),
        "decision": decision,
  }
