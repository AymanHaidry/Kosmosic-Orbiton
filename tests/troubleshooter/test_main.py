"""Test main entry point."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import pytest
from troubleshooter import main


def test_main_runs_flow_1(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "1"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_wont_start", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_2(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "2"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_voice_not_working", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_3(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "3"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_tts_silent", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_4(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "4"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_commands_wrong", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_5(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "5"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_files_projects", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_6(monkeypatch, capsys):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "6"
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    monkeypatch.setattr("troubleshooter.flow_other", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert len(calls) == 2


def test_main_runs_flow_7_no_data(monkeypatch, capsys):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "7")
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    captured = capsys.readouterr()
    assert "No previous scan data" in captured.out


def test_main_restart_loop(monkeypatch):
    calls = []
    def mock_ask(*args, **kwargs):
        calls.append(args)
        if len(calls) == 1:
            return "1"
        if len(calls) == 2:
            return "1"  # post-flow: run another
        if len(calls) == 3:
            return "2"  # second main menu
        return "q"
    monkeypatch.setattr("troubleshooter.ask", mock_ask)
    call_count = {"flow1": 0, "flow2": 0}
    def fake_flow1():
        call_count["flow1"] += 1
        return {}
    def fake_flow2():
        call_count["flow2"] += 1
        return {}
    monkeypatch.setattr("troubleshooter.flow_wont_start", fake_flow1)
    monkeypatch.setattr("troubleshooter.flow_voice_not_working", fake_flow2)
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    assert call_count["flow1"] == 1
    assert call_count["flow2"] == 1


def test_main_invalid_choice_then_valid(monkeypatch, capsys):
    inputs = iter(["99", "1", "q"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    monkeypatch.setattr("troubleshooter.flow_wont_start", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    main()
    captured = capsys.readouterr()
    assert "Please enter one of" in captured.out


def test_main_quit_choice(monkeypatch, capsys):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "q")
    monkeypatch.setattr("builtins.input", lambda: "")
    main()
    captured = capsys.readouterr()
    assert "Stay productive" in captured.out
