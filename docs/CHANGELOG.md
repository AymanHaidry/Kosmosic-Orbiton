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
- Config file system (JSON/YAML) to replace hardcoded `CONFIG` dict
- Plugin architecture for third-party commands
- Resolve self-listening bug (#27) before v1.0
- Resolve Bandit security findings in `troubleshooter.py` (#60) before v1.0



---

 ## [0.7.3] - 2026-06-30
### Fixed
Self-listening bug (#27) — TTS output no longer triggers phantom voice commands
Added tts_active threading event to VoiceManager to track when audio is playing
Added post_tts_until timestamp with 1.5 s silence buffer after TTS finishes
Added is_listening_blocked() method to query TTS + cool-down state
Main loop now skips recognizer.listen() while TTS is active or during post-TTS silence window
Text input commands bypass the silence window entirely (typing always works)
Fixes: "Tokyo motivate me" no longer causes Orbiton to hear its own roast and execute a random follow-up command
Eliminates need for headphones as a workaround for speaker-based setups
### Changed
VoiceManager.__init__ now initializes tts_active, post_tts_until, post_tts_silence, and _lock
VoiceManager._tts_worker wraps _speak_now() in try/finally to guarantee tts_active is always cleared
main() loop reordered: text input → TTS silence check → voice input
CONFIG dict now includes "post_tts_silence": 1.5 for user-tunable silence window duration
### Technical
Thread-safe: post_tts_until is guarded by _lock to prevent race conditions between TTS worker and main loop
Zero new dependencies (no AEC libraries, no webrtcvad, no speexdsp)
Deterministic: mic stays off for exact duration of playback + fixed buffer, unlike previous time.sleep(0.5) workaround which returned too early due to queue-based async TTS

---

## [0.7.1] - 2026-06-14

### Added
- `docs/PROJECT_CONTEXT.md` — comprehensive project context document for contributors and AI tools; covers architecture, key files, dependencies, known issues, roadmap summary, and contributing guide
- `docs/ARCHITECTURE_DECISIONS.md` — full ADR (Architecture Decision Record) log documenting 10 key architectural decisions (ADR-001 through ADR-010)

### Changed
- `website/index.html` — Google Search Console verification tag added for SEO
- `website/` — model lineup updated on project website

### Fixed
- `tests/troubleshooter/main_test.py` — fixed `StopIteration` in `test_main_invalid_choice_then_valid` by providing correct 5-item input sequence to `iter()` (covers: invalid input → valid input → restart → quit → pause prompt)

---

## [0.7.0] - 2026-06-08

### Added
- `troubleshooter.py` — standalone interactive diagnostic tool for diagnosing microphone, TTS, command, and file/project issues
- `tests/troubleshooter/` — 56 new tests across 6 files (colors, input helpers, run_cmd, system checks, fix helpers, diagnostic flows)
- `.github/workflows/troubleshooter.yml` — CI workflow for troubleshooter tests with Codecov coverage
- `docs/TROUBLESHOOT.md` — massively expanded troubleshooting reference (+603 lines)
- `TROUBLESHOOT.md` (root) — quick-reference troubleshooting guide
- Full documentation index table in `README.md` (15 docs listed)
- `## 🔧 Troubleshooting` section in `README.md`

### Changed
- Version bumped `0.6.2` → `0.7.0` across `README.md`, `MANUAL.md`, `website/index.html`, `docs/VERSIONS.md`
- Test suite count updated 151 → 207 in CI workflow
- `requirements.txt` reformatted with section comments
- All root-level doc links in `README.md` updated to `docs/` paths
- `docs/TESTS.md` updated with troubleshooter test category
- `docs/VERSIONS.md` Tokyo-class version range: `1.x.x` → `0.x.x -> 1.x.x`
- `MANUAL.md` version header updated to v0.7

---

## [0.6.2] - 2026-06-07

### Fixed
- **Speech-to-math calculation** — `calculate` command no longer fails on spoken math
  - `MathNormalizer` converts words to digits ("two" → 2, "twenty five" → 25)
  - Spoken operators mapped to symbols ("times", "into", "x" → `*`, "divided by" → `/`, "squared" → `**2`)
  - `safe_eval` whitelist prevents code injection from malformed speech input
  - Fixes: `calculate 2 x 2`, `calculate two times`, `calculate 2 into` all now resolve correctly

### Changed
- `handle_calculate` in `kosmosic_orbiton.py` now routes through `MathNormalizer` instead of raw `eval()`
- `neuro_link_intel.py` exports `MathNormalizer` class

---

## [0.6.1] - 2026-06-07

### Fixed
- **FileDiff workflow** — added `GITHUB_TOKEN` env and `pull-requests: write` permission to fix `Missing required environment variables: GITHUB_TOKEN` error

### Changed
- **CI runs on all branches** — all 10 workflow files updated from `branches: [main, develop]` to `branches: ['*']`
  - compute, core-logic, filediff, integration, launch, pylint, python-tests, python-tests-per-file, system, url-engine
- **Pylint score visibility** — `pylint.yml` now prints score to CI logs via dedicated `Pylint Score` step

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
| Tokyo-class | 0.1.0 → 0.7.1 | Current |
| Odyssey-class | 1.x.x | Planned |
| Genesis-class | 2.x.x | Planned |
| Micron-class | 3.x.x | Planned (ROI-dependent) |
| Aphrodite-class | 4.x.x | Planned |
| Singularity-class | 5.x.x | Vision |
| Utopia-class | 6.x.x | Final Vision |

---

## Release Naming Convention

- **v0.X.Y** — Standard semver
- **v0.X-Tokyo** — Tokyo-class release (current)
- Future: **v1.X-Odyssey**, **v2.X-Genesis**, **vX.X-Singularity**

---

For the full roadmap, see [ROADMAP.md](ROADMAP.md).

---

*Last updated: 2026-06-14 by Orbiton Workflow Agent (scheduled daily health scan)*
