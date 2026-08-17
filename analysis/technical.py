from typing import List, Dict, Optional


def ema(values: List[float], period: int) -> List[float]:
    if len(values) < period:
        return []

    multiplier = 2 / (period + 1)

    result = [sum(values[:period]) / period]

    for price in values[period:]:
        previous = result[-1]
        current = (
            (price - previous) * multiplier
        ) + previous

        result.append(current)

    return result


def rsi(
    closes: List[float],
    period: int = 14,
) -> Optional[float]:

    if len(closes) <= period:
        return None

    gains = []
    losses = []

    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]

        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    average_gain = (
        sum(gains[:period]) / period
    )

    average_loss = (
        sum(losses[:period]) / period
    )

    for i in range(period, len(gains)):
        average_gain = (
            (average_gain * (period - 1))
            + gains[i]
        ) / period

        average_loss = (
            (average_loss * (period - 1))
            + losses[i]
        ) / period

    if average_loss == 0:
        return 100.0

    relative_strength = (
        average_gain / average_loss
    )

    return 100 - (
        100 / (1 + relative_strength)
    )


def true_range(
    high: float,
    low: float,
    previous_close: float,
) -> float:

    return max(
        high - low,
        abs(high - previous_close),
        abs(low - previous_close),
    )


def atr(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14,
) -> Optional[float]:

    if len(closes) <= period:
        return None

    ranges = []

    for i in range(1, len(closes)):
        ranges.append(
            true_range(
                highs[i],
                lows[i],
                closes[i - 1],
            )
        )

    if len(ranges) < period:
        return None

    return sum(
        ranges[-period:]
    ) / period


def analyze_trend(
    closes: List[float],
) -> Dict:

    if len(closes) < 50:
        return {
            "trend": "UNKNOWN",
            "ema_fast": None,
            "ema_slow": None,
        }

    fast = ema(closes, 20)
    slow = ema(closes, 50)

    if not fast or not slow:
        return {
            "trend": "UNKNOWN",
            "ema_fast": None,
            "ema_slow": None,
        }

    fast_value = fast[-1]
    slow_value = slow[-1]

    if fast_value > slow_value:
        trend = "BULLISH"
    elif fast_value < slow_value:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"

    return {
        "trend": trend,
        "ema_fast": fast_value,
        "ema_slow": slow_value,
    }


def technical_analysis(
    highs: List[float],
    lows: List[float],
    closes: List[float],
) -> Dict:

    trend = analyze_trend(closes)

    current_rsi = rsi(closes)

    current_atr = atr(
        highs,
        lows,
        closes,
    )

    score = 0

    if trend["trend"] == "BULLISH":
        score += 40

    elif trend["trend"] == "NEUTRAL":
        score += 20

    if current_rsi is not None:

        if 45 <= current_rsi <= 65:
            score += 30

        elif 30 <= current_rsi < 45:
            score += 20

        elif current_rsi > 70:
            score -= 20

    if current_atr is not None:
        score += 30

    score = max(
        0,
        min(score, 100),
    )

    if score >= 75:
        signal = "STRONG"
    elif score >= 55:
        signal = "WATCH"
    else:
        signal = "WEAK"

    return {
        "trend": trend["trend"],
        "ema_fast": trend["ema_fast"],
        "ema_slow": trend["ema_slow"],
        "rsi": current_rsi,
        "atr": current_atr,
        "technical_score": score,
        "signal": signal,
      }
