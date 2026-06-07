"""Shared fixtures for Orbiton test suite."""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def mock_ui():
    ui = MagicMock()
    ui.error_count = 0
    ui.total_commands = 0
    ui.session_start = MagicMock()
    ui.console = None
    return ui


@pytest.fixture
def mock_voice():
    return MagicMock()


@pytest.fixture
def mock_memory():
    memory = MagicMock()
    memory.learn.return_value = False
    memory.recall.return_value = "I do not know anything about you yet."
    memory.recall_one.return_value = None
    return memory


@pytest.fixture
def mock_intel():
    intel = MagicMock()
    intel.process.return_value = ("", "")
    nlp = MagicMock()
    nlp.normalize.return_value = ""
    intel.nlp = nlp
    return intel


@pytest.fixture
def engine(mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import CommandEngine
    return CommandEngine(mock_ui, mock_voice, mock_memory, mock_intel)


@pytest.fixture
def parser():
    from kosmosic_orbiton import IntentParser
    return IntentParser()
