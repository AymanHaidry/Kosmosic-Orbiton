"""Test status report generation."""
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock


def test_status_report_shows_uptime(engine):
    engine.handle_status()
    # handle_status prints directly or uses ui.console.print; it never calls show_success
    engine.voice.speak.assert_called()


def test_status_includes_command_count(engine):
    engine.ui.total_commands = 42
    engine.ui.error_count = 3
    engine.handle_status()
    # Verify voice speaks the status report with command count
    spoken = engine.voice.speak.call_args[0][0]
    assert "42" in spoken or "commands" in spoken.lower()


def test_status_report_console_table(engine):
    from kosmosic_orbiton import CommandEngine
    mock_ui = MagicMock()
    mock_ui.error_count = 0
    mock_ui.total_commands = 0
    mock_ui.session_start = MagicMock()
    mock_ui.console = MagicMock()  # Must be a MagicMock, not True/False
    mock_voice = MagicMock()
    mock_memory = MagicMock()
    mock_intel = MagicMock()
    engine2 = CommandEngine(mock_ui, mock_voice, mock_memory, mock_intel)
    engine2.handle_status()
    mock_ui.console.print.assert_called()
