"""Test unknown / unrecognized command handling."""
import pytest
from neuro_link import IntentParser, process_text
from unittest.mock import MagicMock


def test_unknown_command_returns_none(parser):
    result = parser.parse("do something completely random")
    assert result is None


def test_gibberish_returns_none(parser):
    result = parser.parse("xyz123 abc !!!")
    assert result is None


def test_empty_string_returns_none(parser):
    result = parser.parse("")
    assert result is None


def test_whitespace_only_returns_none(parser):
    result = parser.parse("   ")
    assert result is None


def test_process_text_unknown_shows_error():
    ui = MagicMock()
    voice = MagicMock()
    memory = MagicMock()
    memory.learn.return_value = False
    intel = MagicMock()
    intel.process.return_value = ("", "")
    from neuro_link import CommandEngine, IntentParser
    engine = CommandEngine(ui, voice, memory, intel)
    parser = IntentParser()
    success, action = process_text("blargh", engine, parser, memory, voice, ui, intel)
    assert success is False
    assert action == ""
    ui.show_error.assert_called()
    voice.speak.assert_called_with("I did not understand that command.")
