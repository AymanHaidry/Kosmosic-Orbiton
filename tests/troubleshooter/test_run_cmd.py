"""Test shell command wrapper."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import pytest
from troubleshooter import run_cmd


def test_echo_success():
    ok, out, err = run_cmd(["echo", "hello"])
    assert ok is True
    assert "hello" in out


def test_nonexistent_command():
    ok, out, err = run_cmd(["definitely_not_a_real_command_12345"])
    assert ok is False


def test_timeout():
    ok, out, err = run_cmd([sys.executable, "-c", "import time; time.sleep(999)"], timeout=0.1)
    assert ok is False
    assert "timed out" in err.lower()


def test_shell_mode():
    ok, out, err = run_cmd("echo hello", shell=True)
    assert ok is True
    assert "hello" in out
