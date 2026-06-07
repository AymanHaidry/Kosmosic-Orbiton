# Orbiton Test Architecture

This document outlines the testing structure for **Orbiton** (by Kosmosic) and the purpose of each test suite.

---

## Directory Structure

```text
tests/
│
├── conftest.py
│
├── core_logic/
│   ├── test_intent_parser.py
│   ├── test_command_patterns.py
│   ├── test_argument_extraction.py
│   └── test_unknown_commands.py
│
├── url_engine/
│   ├── test_search_urls.py
│   ├── test_youtube_urls.py
│   ├── test_maps_urls.py
│   ├── test_weather_urls.py
│   ├── test_airport_urls.py
│   ├── test_track_urls.py
│   ├── test_metar_urls.py
│   └── test_streetview_urls.py
│
├── compute/
│   ├── __init__.py
│   ├── test_basic_math.py
│   ├── test_advanced_math.py
│   ├── test_constants.py
│   ├── test_square_cube.py
│   ├── test_sqrt.py
│   └── test_security.py
│
├── launch/
│   ├── test_open_folders.py
│   ├── test_folder_navigation.py
│   ├── test_latest_file.py
│   ├── test_file_search.py
│   ├── test_project_launch.py
│   ├── test_script_launch.py
│   ├── test_clipboard.py
│   └── test_exam_mode.py
│
├── system/
│   ├── test_status.py
│   ├── test_time.py
│   ├── test_motivation.py
│   ├── test_headphone_detection.py
│   └── test_session_stats.py
│
└── integration/
    ├── test_search_flow.py
    ├── test_youtube_flow.py
    ├── test_weather_flow.py
    ├── test_maps_flow.py
    ├── test_file_open_flow.py
    └── test_project_flow.py
```

---

## Test Categories

### Core Logic

Validates Orbiton's understanding of commands.

#### Coverage

* Intent recognition
* Command pattern matching
* Argument extraction
* Unknown command handling
* Routing decisions

#### Examples

Input:

```text
search airbus a350
```

Expected:

```python
("search", "airbus a350")
```

Input:

```text
weather doha
```

Expected:

```python
("weather", "doha")
```

---

### URL Engine

Validates URL generation without opening browsers.

#### Coverage

* Google Search URLs
* YouTube Search URLs
* Google Maps URLs
* Weather URLs
* Airport Search URLs
* FlightRadar URLs
* METAR URLs
* Street View URLs

#### Examples

Input:

```text
search airbus a350
```

Expected URL:

```text
https://www.google.com/search?q=airbus+a350
```

Input:

```text
track EK568
```

Expected URL contains:

```text
flightradar24.com
```

---

### Compute

Validates mathematical operations and expression parsing.

#### Coverage

* Basic arithmetic
* Advanced calculations
* Constants
* Square and cube operations
* Square root calculations
* Security protections

#### Examples

Input:

```text
2 + 2
```

Expected:

```text
4
```

Input:

```text
sqrt 16
```

Expected:

```text
4
```

---

### Launch

Validates local resource launching and navigation.

#### Coverage

* Folder opening
* Folder traversal
* Latest file discovery
* File searching
* Project launching
* Script execution
* Clipboard actions
* Exam mode setup

#### Examples

Input:

```text
open downloads
```

Expected:

```text
<Path.home()>/Downloads
```

Input:

```text
open project orbiton
```

Expected:

```text
<Project Path>
```

---

### System

Validates utility and system-level functionality.

#### Coverage

* Status reports
* Time retrieval
* Motivation engine
* Headphone detection
* Session statistics

#### Examples

Input:

```text
status report
```

Expected:

```text
Session information returned
```

---

### Integration

Validates complete end-to-end workflows.

#### Coverage

* Search flow
* YouTube flow
* Weather flow
* Maps flow
* File opening flow
* Project launch flow

#### Examples

Input:

```text
search airbus a350
```

Flow:

```text
Voice Input
↓
Intent Parser
↓
URL Engine
↓
Browser Launch Request
```

Expected:

```text
Successful execution
```

---

## CI/CD Integration

Each category can be executed independently through GitHub Actions.

Potential workflow structure:

```text
.github/workflows/

├── core-logic.yml
├── url-engine.yml
├── compute.yml
├── launch.yml
├── system.yml
└── integration.yml
```

Benefits:

* Faster debugging
* Granular status reporting
* Independent subsystem validation
* Separate GitHub badges

---

## Testing Philosophy

Orbiton prioritizes behavior testing over implementation testing.

Instead of testing:

```python
2 + 2 == 4
```

Tests focus on:

```text
User Command
↓
Interpretation
↓
Processing
↓
Result
```

The goal is to verify that Orbiton behaves correctly from the user's perspective while remaining flexible internally.

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# By category
pytest tests/core_logic/ -v
pytest tests/url_engine/ -v
pytest tests/compute/ -v
pytest tests/launch/ -v
pytest tests/system/ -v
pytest tests/integration/ -v
```

---

*Orbiton Test Architecture v1.0 — Kosmosic © 2026*
