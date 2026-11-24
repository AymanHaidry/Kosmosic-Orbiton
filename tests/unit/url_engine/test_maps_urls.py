"""Validate Google Maps URL generation."""
import pytest


def test_maps_url_contains_google_maps(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_maps("times square")
    assert len(opened) == 1
    assert "google.com/maps" in opened[0]
    assert "times" in opened[0]


def test_maps_url_encoding(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_maps("São Paulo")
    assert "google.com/maps" in opened[0]
