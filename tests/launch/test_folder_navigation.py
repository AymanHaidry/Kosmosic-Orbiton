"""Test filesystem navigation."""
import pytest
from pathlib import Path
from unittest.mock import patch


def test_navigate_parent(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_folder_nav("parent")
        assert engine.current_folder == Path.home()
        mock_popen.assert_called_once()


def test_navigate_back(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_folder_nav("back")
        assert engine.current_folder == Path.home()


def test_navigate_up(engine):
    engine.current_folder = Path.home() / "Downloads"
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_folder_nav("up")
        assert engine.current_folder == Path.home()


def test_navigate_subfolder(engine):
    engine.current_folder = Path.home()
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_folder_nav("Downloads")
        assert engine.current_folder == Path.home() / "Downloads"


def test_navigate_nonexistent_shows_error(engine):
    engine.current_folder = Path.home()
    with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_folder_nav("totally_fake_folder_12345")
        engine.ui.show_error.assert_called()
