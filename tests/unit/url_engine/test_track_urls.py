"""Validate Flight Tracking URL generation."""
import pytest


def test_track_url_contains_flightradar(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_track("EK568")
    assert len(opened) == 1
    assert "flightradar24.com" in opened[0]
    assert "EK568" in opened[0]


def test_track_url_cleans_spaces(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_track("ek 568")
    assert "EK568" in opened[0] or "ek568" in opened[0]
