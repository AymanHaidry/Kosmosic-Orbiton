# Test Status

> Live CI status for every test category. See [WORKFLOWS.md](WORKFLOWS.md) for configuration details.

---

## Category Badges

| Category | Status | Files | Tests |
|----------|--------|-------|-------|
| Core Logic | ![Core Logic](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/core-logic.yml/badge.svg) | 4 | ~30 |
| URL Engine | ![URL Engine](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/url-engine.yml/badge.svg) | 8 | ~16 |
| Compute | ![Compute](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/compute.yml/badge.svg) | 7 | ~20 |
| Launch | ![Launch](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/launch.yml/badge.svg) | 8 | ~29 |
| System | ![System](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/system.yml/badge.svg) | 5 | ~15 |
| Integration | ![Integration](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/integration.yml/badge.svg) | 6 | ~12 |
| Pylint | ![Pylint](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/pylint.yml/badge.svg) | — | — |

---

## Per-File Status

### Core Logic (`tests/core_logic/`)

| File | Status | Description |
|------|--------|-------------|
| `test_argument_extraction.py` | ✅ | Multi-word args, empty args, stripping, case preservation |
| `test_command_patterns.py` | ✅ | Regex compilation, no duplicates, pattern variations |
| `test_intent_parser.py` | ✅ | Intent recognition, routing, edge cases |
| `test_unknown_commands.py` | ✅ | Unknown command handling, gibberish, empty input |

### URL Engine (`tests/url_engine/`)

| File | Status | Description |
|------|--------|-------------|
| `test_airport_urls.py` | ✅ | Airport search URL generation |
| `test_maps_urls.py` | ✅ | Google Maps URL encoding |
| `test_metar_urls.py` | ✅ | AviationWeather METAR URL generation |
| `test_search_urls.py` | ✅ | Google Search URL encoding |
| `test_streetview_urls.py` | ✅ | Street View random location URLs |
| `test_track_urls.py` | ✅ | FlightRadar24 URL generation |
| `test_weather_urls.py` | ✅ | Weather search URL generation |
| `test_youtube_urls.py` | ✅ | YouTube search URL generation |

### Compute (`tests/compute/`)

| File | Status | Description |
|------|--------|-------------|
| `test_advanced_math.py` | ✅ | Exponents, modulus, nested parentheses |
| `test_basic_math.py` | ✅ | Addition, subtraction, multiplication, division |
| `test_constants.py` | ✅ | Pi, e, constants in expressions |
| `test_security.py` | ✅ | Malicious input rejection, divide by zero |
| `test_sqrt.py` | ✅ | Square root operations |
| `test_square_cube.py` | ✅ | Squared and cubed operations |

### Launch (`tests/launch/`)

| File | Status | Description |
|------|--------|-------------|
| `test_clipboard.py` | ✅ | Clipboard search integration |
| `test_exam_mode.py` | ✅ | Exam mode activation |
| `test_file_search.py` | ✅ | File search by partial name |
| `test_folder_navigation.py` | ✅ | Filesystem navigation |
| `test_latest_file.py` | ✅ | Latest file discovery |
| `test_open_folders.py` | ✅ | Folder opening by name |
| `test_project_launch.py` | ✅ | VS Code project launching |
| `test_script_launch.py` | ✅ | Python script execution |

### System (`tests/system/`)

| File | Status | Description |
|------|--------|-------------|
| `test_headphone_detection.py` | ✅ | Bluetooth headset detection |
| `test_motivation.py` | ✅ | Toxic motivation engine |
| `test_session_stats.py` | ✅ | Session statistics tracking |
| `test_status.py` | ✅ | Status report generation |
| `test_time.py` | ✅ | Time retrieval |

### Integration (`tests/integration/`)

| File | Status | Description |
|------|--------|-------------|
| `test_file_open_flow.py` | ✅ | End-to-end file opening |
| `test_maps_flow.py` | ✅ | End-to-end maps flow |
| `test_project_flow.py` | ✅ | End-to-end project launch |
| `test_search_flow.py` | ✅ | End-to-end search flow |
| `test_weather_flow.py` | ✅ | End-to-end weather flow |
| `test_youtube_flow.py` | ✅ | End-to-end YouTube flow |

---

## Known Flaky Tests

| Test | Issue | Workaround |
|------|-------|------------|
| `test_navigate_parent` | Platform-specific subprocess mocking | Patched for Windows/Linux |
| `test_open_downloads` | Path.exists() behavior on CI | Mocked Path.exists and is_dir |

---

## Adding a New Test

1. Create `tests/<category>/test_<feature>.py`
2. Add it to the table above
3. Ensure the corresponding workflow in `.github/workflows/` includes the file pattern
4. Run locally: `pytest tests/<category>/test_<feature>.py -v`

See [TESTS.md](TESTS.md) for full architecture details.
