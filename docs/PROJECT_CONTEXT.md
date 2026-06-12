# Project Context — Orbiton by Kosmosic

> This document provides a comprehensive overview of the Orbiton project for new contributors, AI tools, and anyone who needs to quickly understand the codebase.

---

## 🎯 What Is Orbiton?

Orbiton is a **Python-powered desktop voice assistant** that turns your headset into a wireless command terminal. It runs entirely locally (no cloud account required), responds to the wake word **"TOKYO"**, and executes voice or typed commands to:

- Launch apps and open files
- Search the web (Google, YouTube, Maps)
- Perform math calculations (including spoken math)
- Check weather and aviation data (METAR, flight tracking)
- Manage VS Code projects
- Provide knowledge lookups (Wikipedia, built-in facts)
- Motivate you (aggressively)

**Company:** Kosmosic  
**Website:** [theorbiton.vercel.app](https://theorbiton.vercel.app)  
**License:** GNU GPL v3.0  
**Current Version:** v0.7.0 (Tokyo-class)  
**Repository:** [github.com/AymanHaidry/Kosmosic-Orbiton](https://github.com/AymanHaidry/Kosmosic-Orbiton)

---

## 🏗 Repository Structure

```
Kosmosic-Orbiton/
├── kosmosic_orbiton.py          # Main entry point — voice loop, command dispatch
├── neuro_link_intel.py          # Intelligence module — NLP, knowledge, math
├── troubleshooter.py            # Standalone diagnostic tool
├── requirements.txt             # Python dependencies
├── MANUAL.md                    # Complete user manual (root copy)
├── TROUBLESHOOT.md              # Troubleshooting reference (root copy)
├── SECURITY.md                  # Security policy
├── LICENSE.md                   # GPL v3.0
├── docs/                        # Full documentation suite
│   ├── CHANGELOG.md             # Version history (Keep a Changelog format)
│   ├── CODE_OF_CONDUCT.md       # Community standards
│   ├── CONTRIBUTING.md          # Contribution guide
│   ├── CONTRIBUTORS.md          # Contributors list
│   ├── DATA_FILES.md            # Data file formats
│   ├── PHILOSOPHY.md            # Design philosophy
│   ├── ROADMAP.md               # Product roadmap
│   ├── TESTS.md                 # Test architecture
│   ├── TEST_STATUS.md           # CI test status
│   ├── TROUBLESHOOT.md          # Expanded troubleshooting
│   ├── VERSIONS.md              # Versioning system
│   ├── WORKFLOWS.md             # CI/CD docs
│   ├── ARCHITECTURE_DECISIONS.md # ADR log
│   └── PROJECT_CONTEXT.md       # This file
├── tests/                       # pytest suite (207 tests)
│   ├── conftest.py
│   ├── core_logic/              # Intent & pattern tests
│   ├── url_engine/              # URL generation tests
│   ├── compute/                 # Math & security tests
│   ├── launch/                  # File & project tests
│   ├── system/                  # Status & time tests
│   ├── integration/             # End-to-end flow tests
│   └── troubleshooter/          # Troubleshooter tests (56 tests)
├── .github/
│   ├── workflows/               # CI/CD (7 test workflows + pylint)
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   └── release_notes_template.md
└── website/                     # Vercel-hosted project website
```

---

## 🔑 Key Files Explained

### `kosmosic_orbiton.py`
The main application. Contains:
- `CONFIG` dict — all user-configurable settings
- `listen()` — microphone input loop
- `speak()` — Edge TTS output
- `handle_*()` functions — one per command category
- `process_command()` — routes commands to handlers
- `main()` — boot sequence and main loop

### `neuro_link_intel.py`
The intelligence layer. Contains:
- `NaturalLanguageProcessor` — contraction expansion, homophone correction, intent normalization
- `MathNormalizer` — spoken math → Python expression conversion + `safe_eval()`
- `get_intelligence()` — knowledge lookup (built-in facts + Wikimedia API)
- `BUILTIN_INTEL` — moon phases, aviation facts, space facts

### `troubleshooter.py`
Standalone diagnostic tool. Contains:
- `flow_wont_start()` — diagnoses startup failures
- `flow_voice_not_working()` — diagnoses microphone/recognition issues
- `flow_tts_silent()` — diagnoses TTS failures
- `flow_commands_wrong()` — diagnoses command routing issues
- `flow_files_projects()` — diagnoses file/project command failures
- `generate_bug_report()` — creates a bug report file

---

## 🧪 Testing

**Test runner:** pytest  
**Total tests:** 207  
**Coverage:** pytest-cov

```bash
# Run all tests
pytest tests/ -v

# Run by category
pytest tests/core_logic/ -v
pytest tests/url_engine/ -v
pytest tests/compute/ -v
pytest tests/launch/ -v
pytest tests/system/ -v
pytest tests/integration/ -v
pytest tests/troubleshooter/ -v
```

**CI:** GitHub Actions runs each category as a separate job. See `.github/workflows/`.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|--------|
| `SpeechRecognition` | ≥3.10.0 | Voice input (Google Web Speech API) |
| `edge-tts` | ≥6.1.0 | Neural TTS (Microsoft Edge voices) |
| `rich` | ≥13.0.0 | Terminal UI (colors, tables, panels) |
| `pytest` | ≥8.0.0 | Test runner |
| `pytest-cov` | ≥5.0.0 | Coverage reporting |

**Optional (not in requirements.txt):**
- `pyaudio` — Required for microphone input on some platforms
- `bandit` — Security linting (recommended for contributors)

---

## 🚦 Current Status (v0.7.0 — Tokyo-class)

| Area | Status | Notes |
|------|--------|-------|
| Core voice commands | ✅ Stable | 207 tests passing |
| Math engine | ✅ Stable | MathNormalizer handles spoken math |
| Troubleshooter | ✅ New (v0.7.0) | 56 tests, standalone tool |
| Self-listening bug | ⚠️ Partial fix | TTS output can trigger phantom commands — use headphones |
| Bandit security findings | 🔴 Open | 20+ findings in troubleshooter.py — see issue #60 |
| Genesis-class (local LLM) | 🔜 Planned | v2.x roadmap |
| Wake word customization | 🔜 Planned | Post-Tokyo |
| Multi-language support | 🔜 Planned | Post-Tokyo |

---

## 🐛 Known Issues

1. **Self-listening bug** (#27) — TTS output triggers phantom voice commands when using speakers. **Workaround:** Use headphones/headset.
2. **Bandit security findings** (#60) — 20+ `subprocess` and `input()` findings in `troubleshooter.py`. Low real-world risk (local tool), but must be addressed before v1.0.
3. **`help` command unreliable via voice** — Type `help` instead. NLP homophones (`hell`, `halp`, `helf`) partially mitigate.
4. **`exam board` falls through to search** — Say `exam mode` or `exambored` instead.
5. **Version string in `kosmosic_orbiton.py` docstring** — Shows `v0.6.2` but repo is at `v0.7.0`. Cosmetic only.

---

## 🗺 Roadmap Summary

| Class | Version | Key Feature |
|-------|---------|-------------|
| Tokyo-class | v0.x → v1.x | Foundation, voice commands, troubleshooter |
| Odyssey-class | v1.x | Stability, plugin system, wake word customization |
| Genesis-class | v2.x | Local LLM integration (offline AI) |
| Micron-class | v3.x | Lite version (ROI-dependent) |
| Aphrodite-class | v4.x | Email, calls, calendar integration |
| Singularity-class | v5.x | Autonomous intelligence |
| Utopia-class | v6.x | Vision-stage product |

See [ROADMAP.md](ROADMAP.md) for full details.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick summary:

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write tests for new functionality
4. Run `pytest tests/ -v` — all tests must pass
5. Follow Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`
6. Open a PR against `main`

**Code style:** PEP 8, enforced by Pylint CI workflow.

---

## 🔐 Security

See [SECURITY.md](../SECURITY.md) for the vulnerability reporting policy.

**Active security concern:** Bandit findings in `troubleshooter.py` (issue #60). The tool is local-only, reducing real-world attack surface, but findings should be reviewed before v1.0.

---

## 📞 Contact

- **GitHub Issues:** [github.com/AymanHaidry/Kosmosic-Orbiton/issues](https://github.com/AymanHaidry/Kosmosic-Orbiton/issues)
- **Website:** [theorbiton.vercel.app](https://theorbiton.vercel.app)
- **Company:** [kosmosic.vercel.app](https://kosmosic.vercel.app)

---

*Last updated: 2026-06-12 by Orbiton Workflow Agent (scheduled health scan)*
