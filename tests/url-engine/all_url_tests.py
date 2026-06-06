import pytest

from neuro_link import CommandEngine, NeuroInterface

@pytest.fixture
def engine():
ui = NeuroInterface()
return CommandEngine(ui)

============================================================
SEARCH
============================================================

def test_google_search_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_search("airbus a350")

assert len(opened) == 1
assert "google.com/search" in opened[0]
assert "airbus" in opened[0]
============================================================
YOUTUBE
============================================================

def test_youtube_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_youtube("python tutorial")

assert len(opened) == 1
assert "youtube.com/results" in opened[0]
assert "python" in opened[0]
============================================================
WEATHER
============================================================

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
============================================================
AIRPORT
============================================================

def test_airport_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_airport("bengaluru")

assert len(opened) == 1
assert "airport" in opened[0]
============================================================
FLIGHT TRACKING
============================================================

def test_track_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_track("EK568")

assert len(opened) == 1
assert "flightradar24.com" in opened[0]
assert "EK568" in opened[0]
============================================================
METAR
============================================================

def test_metar_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_metar("VOBL")

assert len(opened) == 1
assert "aviationweather" in opened[0]
assert "VOBL" in opened[0]
============================================================
MAPS
============================================================

def test_maps_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_maps("times square")

assert len(opened) == 1
assert "google.com/maps" in opened[0]
============================================================
STREET VIEW
============================================================

def test_streetview_url(engine):
opened = []

engine.open_chrome = lambda url, *args: opened.append(url)

engine.handle_streetview()

assert len(opened) == 1
assert "google.com/maps" in opened[0]
assert "map_action=pano" in opened[0]
