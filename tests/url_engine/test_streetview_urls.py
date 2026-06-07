"""Validate Street View URL generation."""
import pytest


def test_streetview_url_contains_google_maps(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_streetview()
    assert len(opened) == 1
    assert "google.com/maps" in opened[0]
    assert "map_action=pano" in opened[0]


def test_streetview_random_location(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_streetview()
    import re
    assert re.search(r"\d+\.\d+,\s*-?\d+\.\d+", opened[0])
