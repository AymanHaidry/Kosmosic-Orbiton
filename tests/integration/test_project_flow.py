"""End-to-end project launch flow test."""
import pytest
from unittest.mock import patch


def test_project_flow_known(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from neuro_link import process_text
    with patch('neuro_link.subprocess.Popen') as mock_popen:
        success, action = process_text(
            "open project hex link",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_popen.assert_called_once()


def test_project_flow_unknown(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from neuro_link import process_text
    success, action = process_text(
        "open project fake_project",
        engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
    )
    assert success is False
    mock_ui.show_error.assert_called()
