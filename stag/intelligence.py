"""Online knowledge lookup and intent routing for Stag.

No bundled fact database or custom intel directory is loaded. Knowledge is
retrieved from Wikipedia at request time. The HTTP adapter deliberately pins
requests to Wikipedia's HTTPS host and summary endpoint.
"""
import json
from http.client import HTTPSConnection, HTTPException
from urllib.error import URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request


class _WikipediaResponse:
    """Small context-manager response wrapper that closes its connection."""

    def __init__(self, connection, response):
        self._connection = connection
        self.status = response.status
        self._body = response.read()

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self._connection.close()
        return False


def urlopen(request, timeout=6):
    """Open only Wikipedia summary requests, without following arbitrary hosts."""
    parsed = urlsplit(request.full_url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "en.wikipedia.org"
        or parsed.username
        or parsed.password
        or not parsed.path.startswith("/api/rest_v1/page/summary/")
    ):
        raise ValueError("Only Wikipedia page-summary URLs are permitted")

    connection = HTTPSConnection("en.wikipedia.org", timeout=timeout)
    try:
        headers = dict(request.header_items())
        connection.request("GET", parsed.path, headers=headers)
        response = connection.getresponse()
        return _WikipediaResponse(connection, response)
    except (HTTPException, OSError, TimeoutError):
        connection.close()
        raise


class WikipediaClient:
    """Bounded client for Wikipedia's public page-summary endpoint."""

    def search_topic(self, topic):
        topic = (topic or "").strip()
        if not topic:
            return None
        page = quote(topic.replace(" ", "_"), safe="")
        request = Request(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{page}",
            headers={"User-Agent": "StagDesktopAssistant/0.1 (Wikipedia lookup)"},
        )
        try:
            with urlopen(request, timeout=6) as response:
                if isinstance(response.status, int) and response.status != 200:
                    return None
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPException, URLError, TimeoutError, ValueError, OSError):
            return None
        extract = data.get("extract")
        if not isinstance(extract, str) or not extract.strip():
            return None
        title = data.get("title") or topic
        page_url = data.get("content_urls", {}).get("desktop", {}).get(
            "page", f"https://en.wikipedia.org/wiki/{page}"
        )
        return f"{title}: {extract.strip()}\nSource: {page_url}"


class IntelligenceOrchestrator:
    """Routes simple commands and retrieves general knowledge online."""

    def __init__(self):
        from .nlp import NaturalLanguageProcessor
        self.nlp = NaturalLanguageProcessor()
        self.wiki = WikipediaClient()

    def process(self, text):
        normalized = self.nlp.normalize(text)
        if self.nlp.extract_time_query(normalized):
            return "time", None
        weather_city = self.nlp.extract_weather_query(normalized)
        if weather_city:
            return "weather", weather_city
        device_cmd = self.nlp.extract_device_command(normalized)
        if device_cmd:
            return "device", device_cmd
        query = self.nlp.extract_search_query(normalized)
        if query:
            result = self.wiki.search_topic(query)
            if result:
                return "knowledge", result
            return "search", query
        return "unknown", normalized

    def get_random_intel(self):
        return "Ask me about a topic and I will look it up on Wikipedia."

    def get_intel_categories(self):
        return ["Wikipedia"]


_intel = None


def get_intelligence():
    global _intel
    if _intel is None:
        _intel = IntelligenceOrchestrator()
    return _intel
