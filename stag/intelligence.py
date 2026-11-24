"""Online knowledge lookup and intent routing for Stag.

No bundled fact database or custom intel directory is loaded. Knowledge is
retrieved from Wikipedia at request time.
"""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .nlp import NaturalLanguageProcessor


class WikipediaClient:
    """Bounded client for Wikipedia's public page-summary endpoint."""

    BASE_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    def search_topic(self, topic):
        topic = (topic or "").strip()
        if not topic:
            return None
        url = self.BASE_URL + quote(topic.replace(" ", "_"), safe="")
        request = Request(
            url,
            headers={"User-Agent": "StagDesktopAssistant/0.1 (Wikipedia lookup)"},
        )
        try:
            with urlopen(request, timeout=6) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, ValueError, OSError):
            return None
        extract = data.get("extract")
        if not isinstance(extract, str) or not extract.strip():
            return None
        title = data.get("title") or topic
        page_url = data.get("content_urls", {}).get("desktop", {}).get("page", url)
        return f"{title}: {extract.strip()}\\nSource: {page_url}"


class IntelligenceOrchestrator:
    """Routes simple commands and retrieves general knowledge online."""

    def __init__(self):
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
