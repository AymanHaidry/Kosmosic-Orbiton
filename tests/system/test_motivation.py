"""Test toxic motivation engine."""
import pytest


def test_motivate_returns_roast(engine):
    engine.handle_motivate()
    engine.ui.show_roast.assert_called()
    spoken = engine.voice.speak.call_args[0][0]
    assert len(spoken) > 10  # Should be a real sentence


def test_motivate_roast_from_database(engine):
    from neuro_link import TOXIC_ROASTS
    engine.handle_motivate()
    spoken = engine.voice.speak.call_args[0][0]
    assert spoken in TOXIC_ROASTS
