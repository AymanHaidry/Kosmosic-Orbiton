"""Test folder opening by name."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_open_downloads(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("downloads")
        mock_popen.assert_called_once()
        args = mock_popen.call_args[0][0]
        assert Path.home() / "Downloads" in [Path(a) for a in args] or "Downloads" in str(args)


def test_open_documents(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("documents")
        mock_popen.assert_called_once()


def test_open_desktop(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("desktop")
        mock_popen.assert_called_once()


def test_open_pictures(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("pictures")
        mock_popen.assert_called_once()


def test_open_videos(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("videos")
        mock_popen.assert_called_once()


def test_open_music(engine):
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_open_file("music")
        mock_popen.assert_called_once()


def test_open_unknown_folder_falls_back_to_search(engine):
    """Unknown folder name should trigger file search."""
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("nonexistent_folder_xyz")
        assert mock_popen.called or engine.ui.show_error.called
