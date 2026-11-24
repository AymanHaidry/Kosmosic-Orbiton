"""Test folder opening by name."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def _patch_open_explorer():
    """Patch the correct subprocess call based on platform."""
    import sys
    if sys.platform == "win32":
        return patch('kosmosic_orbiton.subprocess.Popen')
    return patch('kosmosic_orbiton.subprocess.run')


def test_open_downloads(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("downloads")
            mock_subprocess.assert_called_once()


def test_open_documents(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("documents")
            mock_subprocess.assert_called_once()


def test_open_desktop(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("desktop")
            mock_subprocess.assert_called_once()


def test_open_pictures(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("pictures")
            mock_subprocess.assert_called_once()


def test_open_videos(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("videos")
            mock_subprocess.assert_called_once()


def test_open_music(engine):
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_open_file("music")
            mock_subprocess.assert_called_once()


def test_open_unknown_folder_falls_back_to_search(engine):
    with _patch_open_explorer() as mock_subprocess,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("nonexistent_folder_xyz")
        assert mock_subprocess.called or engine.ui.show_error.called
