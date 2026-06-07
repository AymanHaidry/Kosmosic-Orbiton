"""Validate every regex pattern in IntentParser."""
import re
import pytest
from kosmosic_orbiton import IntentParser


def test_all_patterns_compile():
    parser = IntentParser()
    for pattern, intent in parser.PATTERNS:
        assert re.compile(pattern), f"Invalid regex for {intent}"


def test_no_duplicate_intents():
    parser = IntentParser()
    intents = [intent for _, intent in parser.PATTERNS]
    assert len(intents) == len(set(intents)), "Duplicate intents detected"


def test_patterns_are_lowercase_anchored():
    parser = IntentParser()
    for pattern, intent in parser.PATTERNS:
        assert pattern.startswith("^"), f"{intent} pattern not anchored"


def test_search_pattern_variations(parser):
    for cmd in ["search python", "google python", "look up python", "find python"]:
        intent, arg = parser.parse(cmd)
        assert intent == "search", f"Failed for: {cmd}"
        assert arg == "python"


def test_youtube_pattern_variations(parser):
    for cmd in ["youtube tutorials", "yt tutorials"]:
        intent, arg = parser.parse(cmd)
        assert intent == "youtube"
        assert arg == "tutorials"


def test_calculate_pattern_variations(parser):
    for cmd in ["calculate 2+2", "compute 2+2", "math 2+2", "solve 2+2"]:
        intent, arg = parser.parse(cmd)
        assert intent == "calculate"


def test_weather_pattern_variations(parser):
    for cmd in ["weather", "weather in doha", "weather at doha", "weather for doha"]:
        intent, arg = parser.parse(cmd)
        assert intent == "weather"


def test_airport_pattern_variations(parser):
    for cmd in ["airport doha", "airports doha", "airport in doha"]:
        intent, arg = parser.parse(cmd)
        assert intent == "airport"


def test_track_pattern_variations(parser):
    for cmd in ["track EK568", "flight EK568", "status of EK568"]:
        intent, arg = parser.parse(cmd)
        assert intent == "track"


def test_open_file_pattern_variations(parser):
    for cmd in ["open downloads", "show downloads", "launch downloads"]:
        intent, arg = parser.parse(cmd)
        assert intent == "open_file"


def test_folder_nav_pattern_variations(parser):
    for cmd in ["go to downloads", "navigate to downloads", "folder downloads", "enter downloads"]:
        intent, arg = parser.parse(cmd)
        assert intent == "folder_nav"


def test_maps_pattern_variations(parser):
    for cmd in ["maps times square", "where is times square", "locate times square"]:
        intent, arg = parser.parse(cmd)
        assert intent == "maps"


def test_exam_mode_variants(parser):
    parser = IntentParser()
    aliases = [
        "exam mode", "focus mode", "launch mode",
        "exambored", "exambord", "exum mode", "eggsam mode"
    ]
    matched = [parser.parse(a) for a in aliases]
    assert matched[0] == ("exam_mode", "")
    # All aliases in the regex now match exam_mode
    assert all(m == ("exam_mode", "") for m in matched)
