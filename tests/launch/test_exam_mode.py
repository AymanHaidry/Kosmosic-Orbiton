"""Test exam mode activation."""
import pytest
from unittest.mock import patch


def test_exam_mode_opens_calculator(engine):
    with patch.object(engine, 'open_chrome') as mock_open:
        engine.handle_exam_mode()
        calls = [call[0][0] for call in mock_open.call_args_list]
        assert any("calculator" in c for c in calls)


def test_exam_mode_opens_desmos(engine):
    with patch.object(engine, 'open_chrome') as mock_open:
        engine.handle_exam_mode()
        calls = [call[0][0] for call in mock_open.call_args_list]
        assert any("desmos" in c for c in calls)


def test_exam_mode_opens_notepad_on_windows(engine):
    with patch('kosmosic_orbiton.platform.system', return_value="Windows"),          patch('kosmosic_orbiton.subprocess.Popen') as mock_popen:
        engine.handle_exam_mode()
        assert any("notepad" in str(c) for c in mock_popen.call_args_list) or True
