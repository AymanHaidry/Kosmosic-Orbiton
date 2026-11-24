# Project Context — Orbiton

This is the maintained architecture reference for the repository.

## Product summary

Orbiton is a Python desktop voice assistant. It accepts spoken commands through SpeechRecognition and typed commands through the terminal. It can open files and applications, search the web, calculate arithmetic, look up weather and aviation data, and control selected device settings.

**Company:** Kosmosic  
**Current release:** 0.8.0 (Tokyo generation)  
**Python:** 3.11+  
**Supported platforms:** Windows, macOS, Linux (some device controls are platform-specific)  
**Launch:** `orbiton` after installation, or `python -m stag` from the repository root.

Speech recognition, Edge neural speech, Wikipedia, and web searches use online services. The user profile is stored locally.

## Repository layout

```text
Orbiton/
├── stag/
│   ├── app.py            # Startup, wake/sleep and input loop
│   ├── commands.py       # CommandEngine and command handlers
│   ├── config.py         # Defaults, shortcuts and help catalogue
│   ├── device.py         # Hardware and operating-system integration
│   ├── intelligence.py   # Wikipedia client and intent routing
│   ├── math_engine.py    # Restricted arithmetic evaluator
│   ├── memory.py         # Local user profile
│   ├── nlp.py            # Speech normalization and extraction
│   ├── parser.py         # Regex intent parser
│   ├── ui.py             # Terminal interface
│   └── voice.py          # Text-to-speech queue and playback
├── docs/                 # Project documentation
├── tests/                # Existing automated test suite
├── website/              # Static website
├── troubleshooter.py     # Interactive diagnostics
├── requirements.txt      # Runtime and current CI dependencies
├── requirements-dev.txt  # Additional developer tools
├── pyproject.toml        # Install metadata and console entry point
└── kosmosic_orbiton.py   # Backward-compatible launcher
```

## Module responsibilities

| Module | Responsibility |
|---|---|
| `stag/app.py` | Initializes services, starts text input and microphone loops, handles wake/sleep state |
| `stag/commands.py` | Implements `CommandEngine` and command handlers |
| `stag/config.py` | Runtime settings, project shortcuts, command catalogue |
| `stag/device.py` | Battery, volume, brightness, Wi-Fi, Bluetooth, system metrics, headset detection |
| `stag/intelligence.py` | Routes simple intents and retrieves Wikipedia summaries |
| `stag/math_engine.py` | Normalizes spoken arithmetic and evaluates a restricted AST |
| `stag/memory.py` | Reads and writes the local user profile |
| `stag/nlp.py` | Contractions, filler removal, homophones, command extraction |
| `stag/parser.py` | Matches text against supported command patterns |
| `stag/ui.py` | Rich terminal presentation with a plain-text fallback |
| `stag/voice.py` | Queued Edge TTS playback and system speech fallback |

## Application flow

1. `stag.app.main()` initializes the UI, voice manager, local profile, command engine, parser, and speech recognizer.
2. Typed input is read on a dedicated thread and forwarded through the same `process_text()` command path as recognized speech.
3. Voice input is captured through SpeechRecognition when a microphone backend is available.
4. `IntelligenceOrchestrator` handles supported high-level intents and live Wikipedia lookup.
5. Commands not handled by that router are matched by `IntentParser`.
6. `CommandEngine` runs the selected handler and reports through the UI and voice manager.

If microphone initialization fails, the application stays open in text-only mode.

## Configuration and local data

Runtime defaults live in `stag/config.py`. The local profile is stored at:

- Windows: `%USERPROFILE%\\.stag\\profile.json`
- macOS/Linux: `~/.stag/profile.json`

A legacy `~/.neuro_link_memory.json` file is copied to the new profile location only when the new file does not already exist. The old file is retained as a backup.

Orbiton no longer loads a bundled static-facts database, custom intel JSON directory, or persistent Wikipedia cache. General knowledge is retrieved from Wikipedia at request time.

## Install and run

```bash
python -m pip install -e .
orbiton
```

Alternative repository launch:

```bash
python -m stag
```

Install developer tools with:

```bash
python -m pip install -r requirements-dev.txt
```

## Compatibility

`kosmosic_orbiton.py` is a thin compatibility launcher for older commands and imports. New code should import from the focused `stag.*` modules.

## Testing status

The existing suite is grouped under `tests/unit/` and `tests/integration/`. Its assertions have not been rewritten for the new module boundaries, and a full test run has not been used as a completion gate for this Cleanup Drive. A dedicated test-rewrite and verification pass follows once the application behavior is settled.
