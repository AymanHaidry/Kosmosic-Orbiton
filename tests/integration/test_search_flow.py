"""End-to-end search flow test."""
import pytest
from unittest.mock import patch, MagicMock


def test_search_flow_full(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text

    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "search airbus a350",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        assert action == ""
        mock_open.assert_called_once()
        mock_ui.show_success.assert_called()
        mock_voice.speak.assert_called()


def test_search_flow_unknown_command(mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text, CommandEngine, IntentParser
    parser = IntentParser()
    engine = CommandEngine(mock_ui, mock_voice, mock_memory, mock_intel)
    success, action = process_text(
        "completely unknown gibberish",
        engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
    )
    assert success is False
    mock_ui.show_error.assert_called()
