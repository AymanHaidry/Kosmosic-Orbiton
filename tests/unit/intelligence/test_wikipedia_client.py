"""Tests for the live Wikipedia client without network access."""
import json
from urllib.error import URLError
from unittest.mock import MagicMock, patch

from stag.intelligence import WikipediaClient


def _response(payload):
    response = MagicMock()
    response.__enter__.return_value = response
    response.read.return_value = json.dumps(payload).encode("utf-8")
    return response


def test_wikipedia_summary_returns_extract_and_source():
    payload = {
        "title": "Jupiter",
        "extract": "Jupiter is the largest planet in the Solar System.",
        "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Jupiter"}},
    }
    with patch("stag.intelligence.urlopen", return_value=_response(payload)) as request:
        result = WikipediaClient().search_topic("Jupiter")

    sent_request = request.call_args.args[0]
    assert "Jupiter" in sent_request.full_url
    assert sent_request.get_header("User-agent").startswith("StagDesktopAssistant/")
    assert "largest planet" in result
    assert "https://en.wikipedia.org/wiki/Jupiter" in result


def test_empty_topic_does_not_make_request():
    with patch("stag.intelligence.urlopen") as request:
        assert WikipediaClient().search_topic("  ") is None
    request.assert_not_called()


def test_wikipedia_network_failure_returns_none():
    with patch("stag.intelligence.urlopen", side_effect=URLError("offline")):
        assert WikipediaClient().search_topic("Jupiter") is None


def test_missing_extract_returns_none():
    with patch("stag.intelligence.urlopen", return_value=_response({"title": "Jupiter"})):
        assert WikipediaClient().search_topic("Jupiter") is None
