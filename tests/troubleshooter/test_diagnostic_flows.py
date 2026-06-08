"""Test diagnostic flow functions."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import pytest
from troubleshooter import (
    flow_wont_start,
    flow_voice_not_working,
    flow_tts_silent,
    flow_commands_wrong,
    flow_files_projects,
    flow_other,
)


# ─── Flow 1: Won't start ───

def test_flow_wont_start_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    results = flow_wont_start()
    assert isinstance(results, dict)
    assert "python_version" in results


def test_flow_wont_start_detects_bad_python(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (False, "3.8.0"))
    results = flow_wont_start()
    assert results["python_version"] is False


def test_flow_wont_start_detects_missing_repo(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (True, "3.11.0"))
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: False)
    results = flow_wont_start()
    assert results["in_repo"] is False


# ─── Flow 2: Voice not working ───

def test_flow_voice_not_working_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_microphone_os", lambda: True)
    monkeypatch.setattr("troubleshooter.check_mic_permissions", lambda: True)
    monkeypatch.setattr("troubleshooter.check_pyaudio", lambda: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    results = flow_voice_not_working()
    assert isinstance(results, dict)
    assert results["typing_works"] is True


def test_flow_voice_not_working_typing_fails_short_circuits(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    results = flow_voice_not_working()
    assert results["typing_works"] is False


def test_flow_voice_not_working_detects_self_listening(monkeypatch):
    inputs = iter([True, True])
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: next(inputs))
    monkeypatch.setattr("troubleshooter.check_microphone_os", lambda: True)
    monkeypatch.setattr("troubleshooter.check_mic_permissions", lambda: True)
    monkeypatch.setattr("troubleshooter.check_pyaudio", lambda: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    results = flow_voice_not_working()
    assert results["self_listening"] is True


# ─── Flow 3: TTS silent ───

def test_flow_tts_silent_returns_dict(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: True)

    def mock_run_cmd(cmd, *args, **kwargs):
        if "edge-tts" in str(cmd):
            (tmp_path / "troubleshooter_test.mp3").write_text("fake")
            return (True, "", "")
        return (True, "", "")

    monkeypatch.setattr("troubleshooter.run_cmd", mock_run_cmd)
    results = flow_tts_silent()
    assert isinstance(results, dict)
    assert "edge_tts" in results


def test_flow_tts_silent_detects_missing_edge_tts(monkeypatch):
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: False)
    results = flow_tts_silent()
    assert results["edge_tts"] is False


# ─── Flow 4: Commands wrong ───

def test_flow_commands_wrong_choice_1_help(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    results = flow_commands_wrong()
    assert results["issue"] == "help_unresponsive"


def test_flow_commands_wrong_choice_2_exam_board(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    results = flow_commands_wrong()
    assert results["issue"] == "exam_board_nlp"


def test_flow_commands_wrong_choice_3_math(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    results = flow_commands_wrong()
    assert "math_tests" in results


def test_flow_commands_wrong_choice_4_project(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "4")
    results = flow_commands_wrong()
    assert "vs_code" in results


def test_flow_commands_wrong_choice_5_clipboard(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "5")
    results = flow_commands_wrong()
    assert results["issue"] == "clipboard"


def test_flow_commands_wrong_choice_6_other(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "6")
    results = flow_commands_wrong()
    assert results["issue"] == "other"


# ─── Flow 5: Files & projects ───

def test_flow_files_projects_choice_1_open_file(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    monkeypatch.setattr("troubleshooter.check_chrome", lambda: True)
    results = flow_files_projects()
    assert isinstance(results, dict)


def test_flow_files_projects_choice_2_project(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    monkeypatch.setattr("troubleshooter.check_vs_code", lambda: True)
    results = flow_files_projects()
    assert isinstance(results, dict)


def test_flow_files_projects_choice_3_run_script(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    results = flow_files_projects()
    assert isinstance(results, dict)


def test_flow_files_projects_choice_4_folder_nav(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "4")
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    results = flow_files_projects()
    assert isinstance(results, dict)


# ─── Flow 6: Other / full scan ───

def test_flow_other_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (True, "3.11.0"))
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_pyaudio", lambda: True)
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_json_file", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: True)
    monkeypatch.setattr("troubleshooter.check_chrome", lambda: True)
    monkeypatch.setattr("troubleshooter.check_vs_code", lambda: True)
    monkeypatch.setattr("troubleshooter.check_microphone_os", lambda: True)
    results = flow_other()
    assert isinstance(results, dict)
    assert "python_version" in results
    assert results["python_version"] is True
