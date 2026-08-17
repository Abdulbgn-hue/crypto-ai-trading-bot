import os
import requests


X_API_TOKEN = os.getenv("X_API_TOKEN")

X_API_URL = "https://api.x.com/2"


def get_user(username: str) -> dict:
    """
    Get public X/Twitter account information.
    Requires X API access token.
    """

    if not X_API_TOKEN:
        return {
            "success": False,
            "enabled": False,
            "error": "X_API_TOKEN is not configured.",
        }

    username = username.lstrip("@").strip()

    headers = {
        "Authorization": f"Bearer {X_API_TOKEN}",
    }

    url = f"{X_API_URL}/users/by/username/{username}"

    params = {
        "user.fields": (
            "description,"
            "created_at,"
            "public_metrics,"
            "verified"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        user = data.get("data")

        if not user:
            return {
                "success": False,
                "enabled": True,
                "error": "X account not found.",
            }

        return {
            "success": True,
            "enabled": True,
            "username": user.get("username"),
            "name": user.get("name"),
            "description": user.get("description"),
            "created_at": user.get("created_at"),
            "verified": user.get("verified"),
            "public_metrics": user.get(
                "public_metrics",
                {}
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "enabled": True,
            "error": str(error),
        }


def get_recent_posts(
    user_id: str,
    max_results: int = 10,
) -> dict:
    """
    Get recent public posts from an X account.
    """

    if not X_API_TOKEN:
        return {
            "success": False,
            "enabled": False,
            "error": "X_API_TOKEN is not configured.",
        }

    headers = {
        "Authorization": f"Bearer {X_API_TOKEN}",
    }

    url = f"{X_API_URL}/users/{user_id}/tweets"

    params = {
        "max_results": max(
            5,
            min(max_results, 100)
        ),
        "tweet.fields": (
            "created_at,"
            "public_metrics,"
            "lang"
        ),
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "enabled": True,
            "posts": data.get(
                "data",
                []
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "enabled": True,
            "error": str(error),
  }
