import requests

from config import (
    MIN_LIQUIDITY_USD,
    MIN_VOLUME_24H_USD,
)


DEX_SEARCH_URL = (
    "https://api.dexscreener.com/latest/dex/search"
)


def search_pairs(query: str) -> list:
    response = requests.get(
        DEX_SEARCH_URL,
        params={"q": query},
        timeout=15,
    )

    response.raise_for_status()

    return response.json().get("pairs", [])


def get_pair_metrics(pair: dict) -> dict:

    liquidity = (
        pair.get("liquidity") or {}
    ).get("usd") or 0

    volume = (
        pair.get("volume") or {}
    ).get("h24") or 0

    price_change = (
        pair.get("priceChange") or {}
    ).get("h24") or 0

    transactions = (
        pair.get("txns") or {}
    ).get("h24") or {}

    return {
        "chain": pair.get("chainId"),
        "dex": pair.get("dexId"),
        "pair_address": pair.get("pairAddress"),
        "base_symbol": (
            pair.get("baseToken") or {}
        ).get("symbol"),
        "base_address": (
            pair.get("baseToken") or {}
        ).get("address"),
        "quote_symbol": (
            pair.get("quoteToken") or {}
        ).get("symbol"),
        "price_usd": pair.get("priceUsd"),
        "liquidity_usd": liquidity,
        "volume_24h_usd": volume,
        "price_change_24h": price_change,
        "buys_24h": transactions.get(
            "buys", 0
        ),
        "sells_24h": transactions.get(
            "sells", 0
        ),
    }


def passes_basic_filters(pair: dict) -> bool:

    metrics = get_pair_metrics(pair)

    return (
        metrics["liquidity_usd"]
        >= MIN_LIQUIDITY_USD
        and
        metrics["volume_24h_usd"]
        >= MIN_VOLUME_24H_USD
    )


def scan_market(query: str) -> list:

    pairs = search_pairs(query)

    valid_pairs = [
        get_pair_metrics(pair)
        for pair in pairs
        if passes_basic_filters(pair)
    ]

    valid_pairs.sort(
        key=lambda item:
        item["liquidity_usd"],
        reverse=True,
    )

    return valid_pairs


def best_pair(query: str):

    pairs = scan_market(query)

    if not pairs:
        return None

    return pairs[0]
