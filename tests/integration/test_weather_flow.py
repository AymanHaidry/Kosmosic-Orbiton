"""End-to-end weather flow test."""
import pytest
from unittest.mock import patch


def test_weather_flow_with_city(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from neuro_link import process_text
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "weather doha",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_open.assert_called_once()
        url = mock_open.call_args[0][0]
        assert "doha" in url


def test_weather_flow_default(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from neuro_link import process_text
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "weather",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_open.assert_called_once()
