"""Test status report generation."""
import pytest
from datetime import datetime
from unittest.mock import patch


def test_status_report_shows_uptime(engine):
    engine.handle_status()
    engine.ui.show_success.assert_called()
    engine.voice.speak.assert_called()


def test_status_includes_command_count(engine):
    engine.ui.total_commands = 42
    engine.ui.error_count = 3
    with patch.object(engine.ui, 'show_success') as mock_show:
        engine.handle_status()
        assert mock_show.called


def test_status_report_console_table(engine, mock_ui):
    from kosmosic_orbiton import CommandEngine
    mock_ui.console = True  # Simulate rich console
    engine2 = CommandEngine(mock_ui, engine.voice, engine.memory, engine.intel)
    engine2.handle_status()
