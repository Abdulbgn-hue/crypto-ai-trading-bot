import os
import requests


ZEROX_API_KEY = os.getenv("ZEROX_API_KEY")

ZEROX_URL = "https://api.0x.org/swap/allowance-holder/price"


def get_quote(
    chain_id: int,
    sell_token: str,
    buy_token: str,
    sell_amount: str,
    taker: str,
) -> dict:
    """
    Get an indicative swap price from 0x.

    This function DOES NOT execute a trade.
    """

    if not ZEROX_API_KEY:
        return {
            "success": False,
            "error": "ZEROX_API_KEY is not configured.",
        }

    params = {
        "chainId": str(chain_id),
        "sellToken": sell_token,
        "buyToken": buy_token,
        "sellAmount": str(sell_amount),
        "taker": taker,
    }

    headers = {
        "0x-api-key": ZEROX_API_KEY,
        "0x-version": "v2",
    }

    try:
        response = requests.get(
            ZEROX_URL,
            params=params,
            headers=headers,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "price": data.get("price"),
            "buy_amount": data.get("buyAmount"),
            "sell_amount": data.get("sellAmount"),
            "gas": data.get("gas"),
            "gas_price": data.get("gasPrice"),
            "issues": data.get("issues", {}),
            "raw": data,
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error),
        }


def calculate_expected_output(
    quote: dict,
) -> float:

    if not quote.get("success"):
        return 0.0

    try:
        return float(
            quote.get("buy_amount", 0)
        )
    except (TypeError, ValueError):
        return 0.0
