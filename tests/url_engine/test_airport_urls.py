"""Validate Airport Search URL generation."""
import pytest


def test_airport_url(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_airport("bengaluru")
    assert len(opened) == 1
    assert "airport" in opened[0]
    assert "bengaluru" in opened[0]
