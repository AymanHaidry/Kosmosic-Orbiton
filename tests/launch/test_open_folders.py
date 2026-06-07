"""Test folder opening by name."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_open_downloads(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("downloads")
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert any("Downloads" in str(a) for a in args)


def test_open_documents(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("documents")
        mock_run.assert_called_once()


def test_open_desktop(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("desktop")
        mock_run.assert_called_once()


def test_open_pictures(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("pictures")
        mock_run.assert_called_once()


def test_open_videos(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("videos")
        mock_run.assert_called_once()


def test_open_music(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run:
        engine.handle_open_file("music")
        mock_run.assert_called_once()


def test_open_unknown_folder_falls_back_to_search(engine):
    with patch('kosmosic_orbiton.subprocess.run') as mock_run,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("nonexistent_folder_xyz")
        assert mock_run.called or engine.ui.show_error.called
