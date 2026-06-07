"""Test clipboard search integration."""
import pytest
from unittest.mock import patch, MagicMock


def test_clipboard_google_search(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="clipboard content here", stderr="")
        with patch.object(engine, 'handle_search') as mock_search:
            engine.handle_clipboard("google")
            mock_search.assert_called_once_with("clipboard content here")


def test_clipboard_youtube_search(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="python tutorial", stderr="")
        with patch.object(engine, 'handle_youtube') as mock_yt:
            engine.handle_clipboard("youtube")
            mock_yt.assert_called_once_with("python tutorial")


def test_empty_clipboard_shows_error(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="")
        engine.handle_clipboard()
        engine.ui.show_error.assert_called_with("Clipboard is empty")
