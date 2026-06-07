"""Test time retrieval."""
import pytest
from datetime import datetime


def test_time_returns_current_time(engine):
    engine.handle_time()
    engine.ui.show_success.assert_called()
    spoken = engine.voice.speak.call_args[0][0]
    assert "is" in spoken.lower()


def test_time_format_12h(engine):
    engine.handle_time()
    spoken = engine.voice.speak.call_args[0][0]
    # Should contain AM or PM
    assert "AM" in spoken or "PM" in spoken or "a.m" in spoken.lower()
