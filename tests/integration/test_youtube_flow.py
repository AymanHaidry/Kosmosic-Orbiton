"""End-to-end YouTube flow test."""
import pytest
from unittest.mock import patch


def test_youtube_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "youtube cockpit landing",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_open.assert_called_once()


def test_youtube_flow_with_nlp(mock_ui, mock_voice, mock_memory, mock_intel):
    """NLP should route youtube queries correctly."""
    from kosmosic_orbiton import process_text, CommandEngine, IntentParser
    mock_intel.process.return_value = ("search", "cockpit landing")
    parser = IntentParser()
    engine = CommandEngine(mock_ui, mock_voice, mock_memory, mock_intel)
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "show me cockpit landing videos",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
