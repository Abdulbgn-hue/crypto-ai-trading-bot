from typing import List, Dict


def calculate_market_score(metrics: Dict) -> int:
    score = 0

    liquidity = metrics.get("liquidity_usd", 0)
    volume = metrics.get("volume_24h_usd", 0)
    change = metrics.get("price_change_24h", 0)
    buys = metrics.get("buys_24h", 0)
    sells = metrics.get("sells_24h", 0)

    # Liquidity
    if liquidity >= 1_000_000:
        score += 30
    elif liquidity >= 250_000:
        score += 25
    elif liquidity >= 100_000:
        score += 20
    elif liquidity >= 50_000:
        score += 10

    # Volume
    if volume >= 1_000_000:
        score += 30
    elif volume >= 250_000:
        score += 25
    elif volume >= 100_000:
        score += 20
    elif volume >= 50_000:
        score += 10

    # Price momentum
    if 2 <= change <= 20:
        score += 20
    elif change > 20:
        score += 10
    elif change < -20:
        score -= 10

    # Buy pressure
    total = buys + sells

    if total > 0:
        buy_ratio = buys / total

        if buy_ratio >= 0.65:
            score += 20
        elif buy_ratio >= 0.55:
            score += 10

    return max(0, min(score, 100))


def rank_markets(markets: List[Dict]) -> List[Dict]:
    ranked = []

    for market in markets:
        item = dict(market)

        item["market_score"] = calculate_market_score(
            item
        )

        ranked.append(item)

    ranked.sort(
        key=lambda item: item["market_score"],
        reverse=True,
    )

    return ranked


def get_top_markets(
    markets: List[Dict],
    limit: int = 10,
) -> List[Dict]:

    ranked = rank_markets(markets)

    return ranked[:limit]
