import re
import requests
from urllib.parse import urljoin, urlparse


USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; CryptoResearchBot/1.0)"
)


def fetch_website(url: str) -> dict:
    """
    Fetch basic public information from a project website.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=15,
            allow_redirects=True,
        )

        response.raise_for_status()

        html = response.text

        # Remove scripts/styles for simpler text extraction
        text = re.sub(
            r"<script.*?</script>",
            " ",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        text = re.sub(
            r"<style.*?</style>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        text = re.sub(
            r"<[^>]+>",
            " ",
            text,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        links = []

        for match in re.findall(
            r'href=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        ):

            absolute_url = urljoin(
                response.url,
                match,
            )

            if absolute_url.startswith(
                ("http://", "https://")
            ):
                links.append(absolute_url)

        unique_links = list(
            dict.fromkeys(links)
        )

        return {
            "success": True,
            "url": response.url,
            "domain": urlparse(
                response.url
            ).netloc,
            "title": extract_title(html),
            "text": text[:15000],
            "links": unique_links[:100],
        }

    except Exception as error:

        return {
            "success": False,
            "url": url,
            "error": str(error),
        }


def extract_title(html: str) -> str:

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return ""

    return re.sub(
        r"\s+",
        " ",
        match.group(1),
    ).strip()
