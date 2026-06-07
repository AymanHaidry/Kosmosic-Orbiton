"""Validate YouTube Search URL generation."""
import pytest


def test_youtube_url_contains_youtube(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_youtube("python tutorial")
    assert len(opened) == 1
    assert "youtube.com/results" in opened[0]
    assert "python" in opened[0]


def test_youtube_url_encoding(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_youtube("C++ tutorials")
    assert "youtube.com/results" in opened[0]
