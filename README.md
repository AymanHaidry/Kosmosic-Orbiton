# Orbiton

A Python desktop voice assistant for hands-free commands, quick web lookups, files, maths, aviation tools, and system controls.

**Company:** Kosmosic  
**Release:** 0.8.0 · Tokyo generation  
**Platforms:** Windows, macOS, Linux  
**Python:** 3.11+

## Get started

1. Install Python 3.11 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install Orbiton:

```bash
python -m pip install -e .
```

5. Start it:

```bash
orbiton
```

You can also launch it without installing the console command:

```bash
python -m stag
```

Orbiton uses Google Speech Recognition for voice input and Edge neural voices when available. These speech services require an internet connection. If a microphone backend is unavailable, the app remains usable in text mode.

## What it can do

- Search Google and YouTube; open Maps and Street View
- Look up weather and aviation information
- Open files, folders, projects, and Python scripts
- Perform spoken arithmetic using a restricted expression evaluator
- Recall user facts saved in a local profile
- Retrieve general knowledge from Wikipedia
- Control supported device settings on Windows and Linux

Say **TOKYO** to wake voice mode. In text mode, type **wake** first.

## Configuration and privacy

Application defaults live in `stag/config.py`. User facts are stored locally at:

- Windows: `%USERPROFILE%\\.stag\\profile.json`
- macOS/Linux: `~/.stag/profile.json`

The profile is not uploaded by Orbiton. Voice recognition, neural speech, Wikipedia lookups, and web searches contact their respective online services. Avoid saving passwords or other sensitive secrets in the profile.

## Project layout

```text
Orbiton/
├── stag/                 # Application package
│   ├── app.py            # Startup and input loop
│   ├── commands.py       # User commands
│   ├── config.py         # Defaults and command descriptions
│   ├── device.py         # OS and hardware integrations
│   ├── intelligence.py   # Online knowledge lookup
│   ├── math_engine.py    # Safe arithmetic
│   ├── memory.py         # Local user profile
│   ├── nlp.py            # Speech normalization
│   ├── parser.py         # Command matching
│   ├── ui.py             # Terminal presentation
│   └── voice.py          # Speech output
├── docs/                 # Architecture and contributor docs
├── tests/                # Automated checks
├── website/              # Project website
├── troubleshooter.py     # Interactive diagnostics
├── requirements.txt      # Runtime and CI dependencies
└── requirements-dev.txt  # Additional developer tools
```

The old `kosmosic_orbiton.py` entry point remains as a compatibility launcher. New setups should use `orbiton` or `python -m stag`.

## Documentation

- [User manual](MANUAL.md)
- [Troubleshooting](TROUBLESHOOT.md)
- [Project architecture](docs/PROJECT_CONTEXT.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)
- [Contributing](docs/CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Development

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Compile the application modules without running the test suite:

```bash
python -m compileall -q stag troubleshooter.py
```

The automated test suite is under `tests/`. Test-suite reorganization is intentionally not part of this Cleanup Drive.

## License

GNU General Public License v3.0. See [LICENSE.md](LICENSE.md).
