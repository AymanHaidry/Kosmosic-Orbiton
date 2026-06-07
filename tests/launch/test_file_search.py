"""Test file search by partial name match."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_file_search_finds_match(engine):
    with patch('kosmosic_orbiton.os.walk') as mock_walk:
        mock_walk.return_value = [
            (str(Path.home()), [], ["report_2024.pdf"])
        ]
        with patch.object(engine, 'open_path') as mock_open:
            engine.handle_open_file("report")
            mock_open.assert_called_once()


def test_file_search_no_match_shows_error(engine):
    with patch('kosmosic_orbiton.os.walk') as mock_walk:
        mock_walk.return_value = []
        engine.handle_open_file("xyz_nonexistent_abc")
        engine.ui.show_error.assert_called()
