"""Test file search by partial name match."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_file_search_finds_match(engine):
    with patch('kosmosic_orbiton.os.walk') as mock_walk,          patch('kosmosic_orbiton.os.stat') as mock_stat:
        mock_walk.return_value = [
            (str(Path.home()), [], ["report_2024.pdf"])
        ]
        mock_stat.return_value = MagicMock(st_mtime=1234567890)
        with patch.object(engine, 'open_path') as mock_open:
            engine.handle_open_file("report")
            mock_open.assert_called_once()


def test_file_search_no_match_shows_error(engine):
    with patch('kosmosic_orbiton.os.walk') as mock_walk:
        mock_walk.return_value = []
        engine.handle_open_file("xyz_nonexistent_abc")
        engine.ui.show_error.assert_called()
