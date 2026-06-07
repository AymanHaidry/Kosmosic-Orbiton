"""End-to-end maps flow test."""
import pytest
from unittest.mock import patch


def test_maps_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from neuro_link import process_text
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "maps times square",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_open.assert_called_once()
        url = mock_open.call_args[0][0]
        assert "google.com/maps" in url
