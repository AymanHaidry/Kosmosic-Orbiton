"""Test ANSI color helpers."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import troubleshooter as ts


def test_ok_contains_green_check():
    out = ts.Colors.ok("python 3.11")
    assert ts.Colors.GREEN in out
    assert "✓" in out
    assert "python 3.11" in out


def test_fail_contains_red_x():
    out = ts.Colors.fail("missing")
    assert ts.Colors.RED in out
    assert "✗" in out


def test_warn_contains_yellow_warning():
    out = ts.Colors.warn("old version")
    assert ts.Colors.YELLOW in out
    assert "⚠" in out


def test_info_contains_blue_info():
    out = ts.Colors.info("note")
    assert ts.Colors.BLUE in out
    assert "ℹ" in out


def test_arrow_contains_cyan_arrow():
    out = ts.Colors.arrow("next step")
    assert ts.Colors.CYAN in out
    assert "→" in out


def test_title_contains_bold_magenta():
    out = ts.Colors.title("DIAGNOSING")
    assert ts.Colors.BOLD in out
    assert ts.Colors.MAGENTA in out
    assert "DIAGNOSING" in out
