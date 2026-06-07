"""Test intent recognition and routing."""
import pytest
from kosmosic_orbiton import IntentParser


def test_search_intent(parser):
    intent, arg = parser.parse("search airbus a350")
    assert intent == "search"
    assert arg == "airbus a350"


def test_youtube_intent(parser):
    intent, arg = parser.parse("youtube cockpit landing")
    assert intent == "youtube"
    assert arg == "cockpit landing"


def test_weather_intent(parser):
    intent, arg = parser.parse("weather doha")
    assert intent == "weather"
    assert arg == "doha"


def test_weather_intent_no_city(parser):
    intent, arg = parser.parse("weather")
    assert intent == "weather"
    assert arg == ""


def test_calculate_intent(parser):
    intent, arg = parser.parse("calculate 25 times 4")
    assert intent == "calculate"
    assert arg == "25 times 4"


def test_airport_intent(parser):
    intent, arg = parser.parse("airport bengaluru")
    assert intent == "airport"
    assert arg == "bengaluru"


def test_track_intent(parser):
    intent, arg = parser.parse("track EK568")
    assert intent == "track"
    assert arg == "ek568"  # Parser lowercases all input


def test_metar_intent(parser):
    intent, arg = parser.parse("metar VOBL")
    assert intent == "metar"
    assert arg == "vobl"  # Parser lowercases all input


def test_maps_intent(parser):
    intent, arg = parser.parse("maps times square")
    assert intent == "maps"
    assert arg == "times square"


def test_streetview_intent(parser):
    intent, arg = parser.parse("streetview")
    assert intent == "streetview"
    assert arg == ""


def test_clipboard_intent(parser):
    intent, arg = parser.parse("clipboard")
    assert intent == "clipboard"
    assert arg == ""


def test_clipboard_youtube_intent(parser):
    intent, arg = parser.parse("clipboard youtube")
    assert intent == "clipboard"
    assert arg == "youtube"


def test_motivate_intent(parser):
    intent, arg = parser.parse("motivate me")
    assert intent == "motivate"
    assert arg == ""


def test_status_intent(parser):
    intent, arg = parser.parse("status report")
    assert intent == "status"
    assert arg == ""


def test_exam_mode_intent(parser):
    intent, arg = parser.parse("exam mode")
    assert intent == "exam_mode"
    assert arg == ""


def test_exam_board_variant(parser):
    """NLP fix: 'exam board' should map to exam_mode via NLP, not raw parser."""
    intent, arg = parser.parse("exam board")
    assert intent is None  # Regex parser does not handle 'exam board' with space


def test_time_intent(parser):
    intent, arg = parser.parse("what time is it")
    assert intent == "time"
    assert arg == ""


def test_kosmosic_intent(parser):
    intent, arg = parser.parse("kosmosic")
    assert intent == "kosmosic"
    assert arg == ""


def test_help_intent(parser):
    intent, arg = parser.parse("help")
    assert intent == "help"
    assert arg == ""


def test_reboot_intent(parser):
    intent, arg = parser.parse("reboot")
    assert intent == "reboot"
    assert arg == ""


def test_whoami_intent(parser):
    intent, arg = parser.parse("who am i")
    assert intent == "whoami"
    assert arg == ""


def test_knowledge_intent(parser):
    intent, arg = parser.parse("tell me about the moon")
    assert intent == "knowledge"
    assert arg == "the moon"


def test_sleep_intent(parser):
    intent, arg = parser.parse("sleep")
    assert intent == "sleep"
    assert arg == ""


def test_wake_intent(parser):
    intent, arg = parser.parse("wake")
    assert intent == "wake"
    assert arg == ""


def test_wake_up_intent(parser):
    intent, arg = parser.parse("wake up")
    assert intent == "wake"
    assert arg == ""
