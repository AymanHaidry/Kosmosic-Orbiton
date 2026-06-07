"""Validate METAR URL generation."""
import pytest


def test_metar_url_contains_aviationweather(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_metar("VOBL")
    assert len(opened) == 1
    assert "aviationweather" in opened[0]
    assert "VOBL" in opened[0]


def test_metar_truncates_to_4_chars(engine):
    """METAR ICAO should be truncated to 4 characters."""
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_metar("VOBL123")
    assert "VOBL" in opened[0]
    assert "VOBL123" not in opened[0]
