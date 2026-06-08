## Tests Architecture

> How Orbiton's test suite is organized, and how to write new tests.

* * *

## Directory Structure

```
tests/
├── conftest.py              # Shared fixtures (engine, parser, mocks)
├── core_logic/              # Intent parsing, command patterns, NLP
├── url_engine/              # URL generation for all web commands
├── compute/                 # Math expressions, security, constants
├── launch/                  # File operations, projects, scripts
├── system/                  # Status, time, motivation, hardware
├── integration/             # End-to-end command flows
└── troubleshooter/          # Diagnostic tool tests
```

* * *

## Categories

### Core Logic (`tests/core_logic/`)

Tests for `IntentParser`, `NaturalLanguageProcessor`, and command routing.

| File | What it tests |
| --- | --- |
| `test_argument_extraction.py` | Multi-word args, empty args, stripping, case, numbers, special chars |
| `test_command_patterns.py` | Regex compilation, no duplicate intents, anchored patterns, variations |
| `test_intent_parser.py` | Intent recognition for all 24+ commands, edge cases |
| `test_unknown_commands.py` | Unknown commands, gibberish, empty/whitespace input |

**Key fixture:** `parser` — fresh `IntentParser()` instance.

### URL Engine (`tests/url_engine/`)

Tests that every command generates the correct URL.

| File | What it tests |
| --- | --- |
| `test_airport_urls.py` | Airport search URL contains city + "airport" |
| `test_maps_urls.py` | Maps URL contains google.com/maps + place |
| `test_metar_urls.py` | METAR URL contains aviationweather + ICAO code |
| `test_search_urls.py` | Search URL contains google.com/search + query |
| `test_streetview_urls.py` | Street View URL contains map_action=pano + coordinates |
| `test_track_urls.py` | Track URL contains flightradar24 + flight number |
| `test_weather_urls.py` | Weather URL contains "weather" + city |
| `test_youtube_urls.py` | YouTube URL contains youtube.com/results + query |

**Pattern:** Each test patches `engine.open_chrome` to capture the URL, then asserts on it.

### Compute (`tests/compute/`)

Tests for the `calculate_expression` utility in `tests/compute/__init__.py`.

| File | What it tests |
| --- | --- |
| `test_advanced_math.py` | Exponents, modulus, nested parentheses |
| `test_basic_math.py` | Addition, subtraction, multiplication, division |
| `test_constants.py` | Pi, e, constants in expressions |
| `test_security.py` | Malicious input rejection, divide by zero, empty input |
| `test_sqrt.py` | Square root operations |
| `test_square_cube.py` | Squared and cubed operations |

**Key fixture:** `calculate_expression` function mirrors `CommandEngine.handle_calculate`.

### Launch (`tests/launch/`)

Tests for file operations, project launching, and script execution.

| File | What it tests |
| --- | --- |
| `test_clipboard.py` | Clipboard read + search integration |
| `test_exam_mode.py` | Exam mode opens calculator, Desmos, notepad |
| `test_file_search.py` | File search by partial name match |
| `test_folder_navigation.py` | Navigate parent, back, up, subfolders |
| `test_latest_file.py` | Latest file discovery by extension |
| `test_open_folders.py` | Open known folders (downloads, documents, etc.) |
| `test_project_launch.py` | VS Code: project launching |
| `test_script_launch.py` | Python script execution |

**Platform note:** Launch tests use `_patch_open_explorer()` helper that patches `subprocess.Popen` on Windows and `subprocess.run` on Linux/macOS.

### System (`tests/system/`)

Tests for system-level features.

| File | What it tests |
| --- | --- |
| `test_headphone_detection.py` | Bluetooth headset detection per OS |
| `test_motivation.py` | Toxic motivation roast selection |
| `test_session_stats.py` | Command count, error count, session tracking |
| `test_status.py` | Status report generation (voice + console) |
| `test_time.py` | Time retrieval and 12h format |

### Integration (`tests/integration/`)

End-to-end tests that run full command flows through `process_text()`.

| File | What it tests |
| --- | --- |
| `test_file_open_flow.py` | Full "open downloads" command flow |
| `test_maps_flow.py` | Full "maps times square" command flow |
| `test_project_flow.py` | Full "open project hex link" command flow |
| `test_search_flow.py` | Full "search airbus a350" command flow |
| `test_weather_flow.py` | Full "weather doha" command flow |
| `test_youtube_flow.py` | Full "youtube cockpit landing" command flow |

### Troubleshooter (`tests/troubleshooter/`)

Tests for the standalone interactive diagnostic tool (`troubleshooter.py`).

| File | What it tests |
| --- | --- |
| `test_colors.py` | ANSI color helpers (✓, ✗, ⚠, ℹ, →, bold/magenta titles) |
| `test_input_helpers.py` | `ask()` and `ask_yes_no()` input validation, EOF handling, defaults |
| `test_run_cmd.py` | `run_cmd()` shell wrapper: success, missing command, timeout, shell mode |
| `test_system_checks.py` | Python version, module imports, file existence, internet, Edge TTS, JSON, microphone, Chrome, VS Code:, PyAudio |
| `test_fix_helpers.py` | `install_module()`, `install_from_requirements()`, `fix_corrupted_json()`, `get_docs_url()`, `generate_bug_report()` |
| `test_diagnostic_flows.py` | All 6 diagnostic flows: wont_start, voice_not_working, tts_silent, commands_wrong, files_projects, other |
| `test_main.py` | Main menu entry point, all 6 flows + bug report, restart loop, invalid choice, quit |

**Critical testing strategy:** All troubleshooter tests mock `input()`, `ask_yes_no()`, and `subprocess.run` to avoid hanging on interactive prompts or failing on CI environments that lack microphones, Chrome, or VS Code:.

* * *

## Fixtures (`conftest.py`)

| Fixture | What it provides |
| --- | --- |
| `mock_ui` | Mocked `NeuroInterface` with counters |
| `mock_voice` | Mocked `VoiceManager` |
| `mock_memory` | Mocked `UserMemory` (learn returns False by default) |
| `mock_intel` | Mocked `IntelligenceOrchestrator` |
| `engine` | `CommandEngine` built from mocks |
| `parser` | Fresh `IntentParser()` |

* * *

## Writing a New Test

### For a new URL-opening command

```python
# tests/url_engine/test_translate_urls.py
import pytest

def test_translate_url(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_translate("hello world")
    assert len(opened) == 1
    assert "translate.google.com" in opened[0]
    assert "hello" in opened[0]
```

### For a new intent

```python
# tests/core_logic/test_intent_parser.py
def test_translate_intent(parser):
    intent, arg = parser.parse("translate hello to french")
    assert intent == "translate"
    assert arg == "hello to french"
```

### For a new file operation

```python
# tests/launch/test_translate_flow.py
import pytest
from unittest.mock import patch
from pathlib import Path

def test_translate_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(engine, 'open_chrome') as mock_open:
        success, action = process_text(
            "translate hello world",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success is True
        mock_open.assert_called_once()
```

### For a new troubleshooter diagnostic

```python
# tests/troubleshooter/test_diagnostic_flows.py
import pytest
from troubleshooter import flow_wont_start

def test_new_flow_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "", ""))
    results = flow_wont_start()
    assert isinstance(results, dict)
    assert "python_version" in results
```

**Critical rule:** Always mock `builtins.input`, `troubleshooter.ask`, and `troubleshooter.ask_yes_no`. The troubleshooter is designed for interactive terminal use; tests must simulate all user responses and external command outputs.

* * *

## Running Tests

```bash
# All tests
pytest tests/ -v

# Single category
pytest tests/core_logic/ -v
pytest tests/url_engine/ -v
pytest tests/compute/ -v
pytest tests/launch/ -v
pytest tests/system/ -v
pytest tests/integration/ -v
pytest tests/troubleshooter/ -v

# Single file
pytest tests/launch/test_folder_navigation.py -v
pytest tests/troubleshooter/test_system_checks.py -v

# Single test
pytest tests/launch/test_folder_navigation.py::test_navigate_parent -v
pytest tests/troubleshooter/test_diagnostic_flows.py::test_flow_wont_start_returns_dict -v

# With coverage
pytest tests/ -v --cov=kosmosic_orbiton --cov=troubleshooter --cov-report=xml
```

* * *

## CI Workflows

Each category has its own workflow in `.github/workflows/`. See WORKFLOWS.md for details.

| Workflow | File | Runs on |
| --- | --- | --- |
| `core-logic.yml` | `tests/core_logic/` | Ubuntu |
| `url-engine.yml` | `tests/url_engine/` | Ubuntu |
| `compute.yml` | `tests/compute/` | Ubuntu |
| `launch.yml` | `tests/launch/` | Windows |
| `system.yml` | `tests/system/` | Ubuntu |
| `integration.yml` | `tests/integration/` | Ubuntu |
| `troubleshooter.yml` | `tests/troubleshooter/` | Ubuntu |
| `pylint.yml` | `kosmosic_orbiton.py` + `neuro_link_intel.py` + `troubleshooter.py` | Ubuntu |

* * *

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` | `kosmosic_orbiton` not in path | `conftest.py` adds repo root to `sys.path` |
| `subprocess` patch fails on Windows | Wrong patch target | Use `_patch_open_explorer()` helper |
| `Path.exists()` returns False in CI | CI doesn't have real folders | Mock `Path.exists` and `Path.is_dir` |
| Voice tests fail | No microphone in CI | Use screen recordings, not unit tests |
| Troubleshooter tests hang | `input()` not mocked | Monkeypatch `builtins.input`, `troubleshooter.ask`, and `troubleshooter.ask_yes_no` |
| Troubleshooter tests fail on macOS/Windows | Platform-specific checks (e.g. `arecord`, `Get-PnpDevice`) | Mock `sys.platform` and `run_cmd()` return values |
| Troubleshooter import error | `tests/troubleshooter/__init__.py` shadows root `troubleshooter.py` | Do **not** create `tests/troubleshooter/__init__.py` |
| Troubleshooter coverage low | `troubleshooter.py` is standalone | Add `--cov=troubleshooter` to pytest flags |

* * *

See TEST_STATUS.md for current CI status.
