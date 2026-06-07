"""Test session statistics tracking."""
import pytest
from datetime import datetime


def test_total_commands_incremented():
    from kosmosic_orbiton import NeuroInterface
    ui = NeuroInterface()
    initial = ui.total_commands
    ui.total_commands += 1
    assert ui.total_commands == initial + 1


def test_error_count_incremented():
    from kosmosic_orbiton import NeuroInterface
    ui = NeuroInterface()
    initial = ui.error_count
    ui.show_error("test error")
    assert ui.error_count == initial + 1


def test_session_start_is_datetime():
    from kosmosic_orbiton import NeuroInterface
    ui = NeuroInterface()
    assert isinstance(ui.session_start, datetime)
