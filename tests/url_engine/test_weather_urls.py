"""Validate Weather URL generation."""
import pytest


def test_weather_city_url(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_weather("doha")
    assert len(opened) == 1
    assert "weather" in opened[0]
    assert "doha" in opened[0]


def test_weather_default_url(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_weather()
    assert len(opened) == 1
    assert "weather" in opened[0]
