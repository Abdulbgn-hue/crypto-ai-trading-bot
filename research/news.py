import os
import requests


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_API_URL = "https://newsapi.org/v2/everything"


def search_news(
    query: str,
    language: str = "en",
    page_size: int = 10,
) -> dict:
    """
    Search public news related to a crypto project/token.

    Requires NEWS_API_KEY.
    """

    if not NEWS_API_KEY:
        return {
            "success": False,
            "enabled": False,
            "error": "NEWS_API_KEY is not configured.",
            "articles": [],
        }

    params = {
        "q": query,
        "language": language,
        "pageSize": min(page_size, 100),
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        articles = []

        for article in data.get("articles", []):
            articles.append(
                {
                    "title": article.get("title"),
                    "description": article.get(
                        "description"
                    ),
                    "url": article.get("url"),
                    "source": (
                        article.get("source") or {}
                    ).get("name"),
                    "published_at": article.get(
                        "publishedAt"
                    ),
                }
            )

        return {
            "success": True,
            "enabled": True,
            "total_results": data.get(
                "totalResults",
                len(articles),
            ),
            "articles": articles,
        }

    except Exception as error:
        return {
            "success": False,
            "enabled": True,
            "error": str(error),
            "articles": [],
  }
