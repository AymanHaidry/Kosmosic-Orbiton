"""Validate Google Search URL generation."""
import pytest


def test_search_url_contains_google(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_search("airbus a350")
    assert len(opened) == 1
    assert "google.com/search" in opened[0]
    assert "airbus" in opened[0]
    assert "a350" in opened[0]


def test_search_url_encoding(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_search("C++ programming")
    assert "%2B%2B" in opened[0] or "++" in opened[0]


def test_search_empty_query(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_search("")
    assert len(opened) == 1
    assert "google.com/search" in opened[0]
