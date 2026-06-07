"""Test latest file discovery."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_latest_pdf(engine):
    with patch.object(engine, 'find_latest_file', return_value=Path.home() / "test.pdf") as mock_find,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("latest pdf")
        mock_find.assert_called_once()


def test_latest_word(engine):
    with patch.object(engine, 'find_latest_file', return_value=Path.home() / "test.docx") as mock_find,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("latest word")
        mock_find.assert_called_once()


def test_latest_python(engine):
    with patch.object(engine, 'find_latest_file', return_value=Path.home() / "test.py") as mock_find,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("latest python")
        mock_find.assert_called_once()


def test_latest_excel(engine):
    with patch.object(engine, 'find_latest_file', return_value=Path.home() / "test.xlsx") as mock_find,          patch.object(engine, 'open_path') as mock_open:
        engine.handle_open_file("latest excel")
        mock_find.assert_called_once()


def test_latest_no_files_shows_error(engine):
    with patch.object(engine, 'find_latest_file', return_value=None) as mock_find:
        engine.handle_open_file("latest pdf")
        engine.ui.show_error.assert_called()
