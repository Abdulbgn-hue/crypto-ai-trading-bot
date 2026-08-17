from typing import List, Dict

from scanner.dex import search_pairs, get_pair_metrics
from scanner.market import calculate_market_score


def discover_tokens(
    queries: List[str],
    limit_per_query: int = 20,
) -> List[Dict]:
    """
    Search multiple market queries and return
    ranked DEX opportunities.
    """

    opportunities = []
    seen_pairs = set()

    for query in queries:
        try:
            pairs = search_pairs(query)

            for pair in pairs[:limit_per_query]:
                pair_address = pair.get("pairAddress")

                if not pair_address:
                    continue

                if pair_address in seen_pairs:
                    continue

                seen_pairs.add(pair_address)

                metrics = get_pair_metrics(pair)

                score = calculate_market_score(metrics)

                metrics["market_score"] = score

                opportunities.append(metrics)

        except Exception as error:
            print(
                f"Discovery error for {query}: {error}"
            )

    opportunities.sort(
        key=lambda item: item["market_score"],
        reverse=True,
    )

    return opportunities


def get_best_opportunities(
    queries: List[str],
    minimum_score: int = 60,
    limit: int = 10,
) -> List[Dict]:
    """
    Return only opportunities above the
    minimum market score.
    """

    opportunities = discover_tokens(queries)

    filtered = [
        opportunity
        for opportunity in opportunities
        if opportunity["market_score"]
        >= minimum_score
    ]

    return filtered[:limit]
