# Changelog

All notable changes to Orbiton will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Genesis-class intelligence (local LLM integration)
- Micron-class lite version (ROI-dependent)
- Email, calls, calendar (post-Genesis / ~v4.0)
- Wake word customization
- Multi-language support
- IoT integration
- Auth system (online accounts)
- Website for downloads and intel sharing

---

## [0.6.0] - 2026-06-07

### Fixed
- CI/CD pipeline now passes all 151 tests across 7 workflows
- Platform-aware subprocess mocking for Windows/Linux/macOS
- `Path.exists()` and `Path.is_dir()` mocking in launch tests
- Self-listening bug partially mitigated (TTS output no longer triggers random intel)

### Changed
- Test suite reorganized into 6 categories: core_logic, url_engine, compute, launch, system, integration
- Each category runs as separate CI job for visibility
- Pylint workflow added for code quality

---

## [0.5.0] - 2026-06-07

### Removed
- **Constellations knowledge dataset** from built-in intelligence module
  - Orion, Ursa Major, Cassiopeia, Scorpius, Cygnus, Leo, Andromeda, Crux
  - Why: Reduces bundle size. Constellation queries now route to Wikimedia/Wikipedia REST API
  - Still built-in: Moon Phases, Aviation Facts, Space Facts

### Changed
- Cleaner `BUILTIN_INTEL` structure with one fewer nested dictionary
- Reduced memory footprint on startup
- Backward compatibility maintained for all other lookups

---

## [0.4.0] - 2026-06-06

### Added
- **Dedicated `neuro_link_intel.py` module** — separated NLP and knowledge processing from main application
- **Natural Language Processor (NLP)** layer:
  - Contraction expansion ("what's" → "what is")
  - Homophone correction ("exambored" → "exam mode", "hell" → "help")
  - Intent normalization and query cleanup
- **File Explorer integration** — folders open directly in Windows Explorer with numbered file list
- **Apple-style boot sequence** — minimalist "● → Loading → ✓ Ready" startup
- **Built-in knowledge base**:
  - Constellations (Orion, Ursa Major, Cassiopeia, Scorpius, Cygnus, Leo, Andromeda, Crux)
  - Moon Phases (8 phases with descriptions)
  - Aviation Facts (V1, V2, Mach, ICAO, Squawk, METAR, TAF, etc.)
  - Space Facts (ISS, Mars, Black Holes, Light Years, Big Bang, etc.)
- **Wikimedia integration** — Wikipedia REST API + caching for dynamic fact retrieval
- **Manual sleep and wake controls**:
  - Sleep: `sleep`, `go to sleep`, `shut down`
  - Wake: `Tokyo`, `wake`, `wake up`, `start`, `online`
- **Reboot system** — reliable relaunching via `subprocess.Popen` instead of `os.execl`

### Changed
- Removed automatic sleep functionality (no more `wake_misses` / `sleep_after_misses`)
- Orbiton remains active indefinitely until explicit sleep command
- Help recognition expanded: `help`, `hell`, `hellp`, `halp`, `helf`, `elpe`
- Exam mode recognition expanded: `exam mode`, `exambored`, `exambord`, `exum mode`, `eggsam mode`

### Fixed
- Reboot reliability on Windows
- Help command misheard variants now correctly routed

---

## [0.3.0] - 2026-06-06

### Added
- Initial voice command framework
- URL launcher system (Google, YouTube, Maps, FlightRadar24, etc.)
- VS Code project launcher
- Aviation utilities (METAR, TAF, airport search, flight tracking)
- Calculator engine with natural language math
- File navigation features
- JBL headset workflow foundation
- Toxic motivation engine (roasts)
- Session status and time commands
- User memory system (learns facts about you)

---

## [0.2.0] - 2026-06-06

### Added
- Basic speech recognition integration
- Terminal UI with rich formatting
- Wake word detection ("Tokyo")
- Cross-platform subprocess handling (Windows, macOS, Linux)

---

## [0.1.0] - 2026-06-06

### Added
- Initial project structure
- Basic command parsing
- Proof-of-concept voice input

---

## Model Class History

| Class | Version | Status |
|-------|---------|--------|
| Tokyo-class | 0.1.0 → 0.6.0 | Current |
| Genesis-class | — | Planned |
| Micron-class | — | Planned (ROI-dependent) |
| Singularity-class | — | Vision |

---

## Release Naming Convention

- **v0.X.Y** — Standard semver
- **v0.X-Tokyo** — Tokyo-class release (current)
- Future: **v1.X-Genesis**, **v2.X-Micron**, **vX.X-Singularity**

---

For the full roadmap, see [ROADMAP.md](ROADMAP.md).
