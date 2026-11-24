"""Test input helpers."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import pytest
from troubleshooter import ask, ask_yes_no


def test_ask_strips_and_lowercases(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "  YES  ")
    assert ask("continue?") == "yes"


def test_ask_validates_options(monkeypatch):
    inputs = iter(["maybe", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask("pick:", ["1", "2", "3"]) == "2"


def test_ask_eof_raises_system_exit(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(EOFError()))
    with pytest.raises(SystemExit):
        ask("?")


def test_ask_yes_no_defaults_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert ask_yes_no("ok?", default="y") is True


def test_ask_yes_no_defaults_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert ask_yes_no("ok?", default="n") is False


def test_ask_yes_no_accepts_y(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert ask_yes_no("ok?") is True


def test_ask_yes_no_accepts_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "no")
    assert ask_yes_no("ok?") is False


def test_ask_yes_no_rejects_invalid_then_accepts(monkeypatch):
    inputs = iter(["maybe", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert ask_yes_no("ok?") is True
