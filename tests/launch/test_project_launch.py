"""Test VS Code project launching."""
import pytest
from unittest.mock import patch


def test_open_known_project(engine):
    with patch('neuro_link.subprocess.Popen') as mock_popen:
        engine.handle_project("hex link")
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert "code" in args[0] or any("hex" in str(a).lower() for a in args)


def test_open_unknown_project_shows_error(engine):
    with patch('neuro_link.subprocess.Popen') as mock_popen:
        engine.handle_project("unknown_project_xyz")
        engine.ui.show_error.assert_called()
        engine.voice.speak.assert_called_with("I could not find the project unknown_project_xyz.")
