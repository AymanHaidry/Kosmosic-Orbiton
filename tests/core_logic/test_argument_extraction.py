"""Test argument extraction edge cases."""
import pytest
from kosmosic_orbiton import IntentParser


def test_extracts_multi_word_args(parser):
    intent, arg = parser.parse("search airbus a350 specifications")
    assert arg == "airbus a350 specifications"


def test_extracts_empty_arg(parser):
    intent, arg = parser.parse("weather")
    assert arg == ""


def test_strips_leading_trailing_spaces(parser):
    intent, arg = parser.parse("search   spaced out   ")
    assert arg == "spaced out"


def test_preserves_case_in_args(parser):
    intent, arg = parser.parse("search Airbus A350")
    assert arg == "airbus a350"


def test_numeric_args(parser):
    intent, arg = parser.parse("calculate 100 divided by 5")
    assert arg == "100 divided by 5"


def test_icao_code_arg(parser):
    intent, arg = parser.parse("metar VOBL")
    assert arg == "vobl"


def test_flight_number_arg(parser):
    intent, arg = parser.parse("track EK568")
    assert arg == "ek568"


def test_special_chars_in_args(parser):
    intent, arg = parser.parse("search C++ programming")
    assert arg == "c++ programming"
