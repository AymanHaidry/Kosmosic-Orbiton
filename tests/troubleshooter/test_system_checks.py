"""Test system diagnostic checks."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import json
import pytest
from pathlib import Path
from troubleshooter import (
    check_python_version,
    check_module,
    check_file_exists,
    check_internet,
    check_edge_tts_connectivity,
    check_json_file,
    check_microphone_os,
    check_mic_permissions,
    check_chrome,
    check_vs_code,
    check_pyaudio,
)


def test_check_python_version_returns_tuple():
    ok, ver = check_python_version()
    assert isinstance(ok, bool)
    assert isinstance(ver, str)
    parts = ver.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_check_module_existing():
    assert check_module("os") is True


def test_check_module_missing():
    assert check_module("definitely_fake_module_12345") is False


def test_check_module_import_name_override():
    ok = check_module("speechrecognition", "speech_recognition")
    assert ok in (True, False)


def test_check_file_exists_found(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hi")
    assert check_file_exists(str(f), "test file") is True


def test_check_file_exists_missing(tmp_path):
    assert check_file_exists(str(tmp_path / "nope.txt"), "nope") is False


def test_check_internet_returns_bool():
    assert isinstance(check_internet(), bool)


def test_check_edge_tts_connectivity_returns_bool():
    assert isinstance(check_edge_tts_connectivity(), bool)


def test_check_json_file_valid(tmp_path):
    f = tmp_path / "good.json"
    f.write_text(json.dumps({"key": "val"}))
    assert check_json_file(str(f)) is True


def test_check_json_file_missing_warns(tmp_path):
    assert check_json_file(str(tmp_path / "missing.json")) is True


def test_check_json_file_corrupted(tmp_path):
    f = tmp_path / "bad.json"
    f.write_text("{not json")
    assert check_json_file(str(f)) is False


def test_check_microphone_os_returns_bool_or_none():
    assert check_microphone_os() in (True, False, None)


def test_check_mic_permissions_returns_bool_or_none():
    assert check_mic_permissions() in (True, False, None)


def test_check_chrome_returns_bool():
    assert isinstance(check_chrome(), bool)


def test_check_vs_code_returns_bool():
    assert isinstance(check_vs_code(), bool)


def test_check_pyaudio_returns_bool():
    assert isinstance(check_pyaudio(), bool)
