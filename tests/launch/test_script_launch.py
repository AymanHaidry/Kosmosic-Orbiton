"""Test Python script execution."""
import pytest
from pathlib import Path
from unittest.mock import patch


def test_run_script_found(engine):
    with patch('kosmosic_orbiton.Path.rglob') as mock_rglob:
        mock_script = Path.home() / "test_script.py"
        mock_rglob.return_value = [mock_script]
        with patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
            engine.handle_run("test_script")
            mock_popen.assert_called_once()


def test_run_script_not_found_shows_error(engine):
    with patch('kosmosic_orbiton.Path.rglob') as mock_rglob:
        mock_rglob.return_value = []
        engine.handle_run("nonexistent_script")
        engine.ui.show_error.assert_called()
