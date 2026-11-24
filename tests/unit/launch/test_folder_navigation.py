"""Test filesystem navigation."""
import pytest
from pathlib import Path
from unittest.mock import patch


def _patch_open_explorer():
    """Patch the correct subprocess call based on platform."""
    import sys
    if sys.platform == "win32":
        return patch('kosmosic_orbiton.subprocess.Popen')
    return patch('kosmosic_orbiton.subprocess.run')


def test_navigate_parent(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_folder_nav("parent")
            assert engine.current_folder == Path.home()
            mock_subprocess.assert_called_once()


def test_navigate_back(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_folder_nav("back")
            assert engine.current_folder == Path.home()


def test_navigate_up(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_folder_nav("up")
            assert engine.current_folder == Path.home()


def test_navigate_subfolder(engine):
    engine.current_folder = Path.home()
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            engine.handle_folder_nav("Downloads")
            # handle_folder_nav lowercases the target
            assert engine.current_folder == Path.home() / "downloads"


def test_navigate_nonexistent_shows_error(engine):
    engine.current_folder = Path.home()
    with _patch_open_explorer() as mock_subprocess:
        engine.handle_folder_nav("totally_fake_folder_12345")
        engine.ui.show_error.assert_called()
