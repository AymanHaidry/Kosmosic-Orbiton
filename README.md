# 🎧 Orbiton — Voice Command Terminal

> *"We put the world around your head."*

**Company:** [Kosmosic](https://kosmosic.vercel.app)  
**Product:** Orbiton  
**Wake Word:** TOKYO  
**Current Class:** [Tokyo-class](ROADMAP.md#tokyo-class-current)

Orbiton is a Python-powered desktop voice assistant that turns your headset into a wireless command terminal. Launch apps, search the web, open files, manage projects, and automate everyday tasks using natural voice commands. No cloud required. No bloat. Just you and your machine.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmosic-Orbiton

# Install dependencies
pip install -r requirements.txt  # speech_recognition, edge-tts, rich, etc.

# Run Orbiton
python kosmosic_orbiton.py
```

Say **"TOKYO"** to wake the assistant, or type commands directly in the terminal.

---

## 🎯 CI Status

| Category | Status |
|----------|--------|
| Core Logic | ![Core Logic](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/core-logic.yml/badge.svg) |
| URL Engine | ![URL Engine](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/url-engine.yml/badge.svg) |
| Compute | ![Compute](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/compute.yml/badge.svg) |
| Launch | ![Launch](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/launch.yml/badge.svg) |
| System | ![System](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/system.yml/badge.svg) |
| Integration | ![Integration](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/integration.yml/badge.svg) |
| Pylint | ![Pylint](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/pylint.yml/badge.svg) |

See [TEST_STATUS.md](TEST_STATUS.md) for per-test details and [WORKFLOWS.md](WORKFLOWS.md) for CI configuration.

---

## 🎤 Voice Commands

| Category | Command | Description |
|----------|---------|-------------|
| 🔍 Search | `search <query>` | Google search |
| 🎥 YouTube | `youtube <query>` | Search YouTube |
| 🧮 Math | `calculate <expr>` | Calculate and speak result — now understands spoken math: "two times two", "twenty five divided by five", "three squared" |
| 🌤 Weather | `weather [city]` | Check weather |
| ✈️ Airport | `airport <city>` | Search airport info |
| 🛫 Track | `track <flight>` | Track flight on FlightRadar24 |
| 📡 METAR | `metar <icao>` | Aviation weather report |
| 📂 Files | `open <folder/file>` | Open files or folders |
| 📁 Navigate | `go to <folder>` | Navigate filesystem |
| 💻 Projects | `open project <name>` | Open VS Code project |
| 🐍 Run | `run <script>` | Run Python script |
| 🗺 Maps | `maps <place>` | Google Maps search |
| 🌍 Street View | `streetview` | Random amazing place |
| 📋 Clipboard | `clipboard [youtube]` | Search clipboard content |
| 💪 Motivate | `motivate me` | Toxic motivation roast |
| 📊 Status | `status report` | Session statistics |
| 🎓 Exam Mode | `exam mode` | Launch study tools |
| 🕐 Time | `what time is it` | Current time |
| 🧠 Memory | `who am i` | Recall stored user info |
| 📚 Intel | `tell me about <topic>` | Knowledge lookup |
| 🔄 Reboot | `reboot` | Restart Orbiton |
| 😴 Sleep | `sleep` | Put Orbiton to sleep |
| ☀️ Wake | `wake` / `wake up` / say **TOKYO** | Wake Orbiton |
| 🎓 Kosmosic | `kosmosic` | Open study dashboard |

---

## 🧠 Intelligence Module

Orbiton includes a pluggable intelligence system (`neuro_link_intel.py`) that handles:

- **NLP normalization** — "what's" → "what is", "exam board" → "exam mode"
- **Knowledge lookup** — constellations, moon phases, aviation facts, space facts
- **Wikimedia scraping** — live Wikipedia/Wiktionary queries with local caching
- **Contextual routing** — decides whether to search, calculate, or answer directly
- **Homophone correction** — handles misheard commands like "exambored" → "exam mode"
- **Math normalization** — `MathNormalizer` converts spoken math ("two times", "divided by", "x") into safe Python expressions before evaluation

Read more in [PHILOSOPHY.md](PHILOSOPHY.md).

---

## 🧪 Testing

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
```

See [TESTS.md](TESTS.md) for the full test architecture and [TEST_STATUS.md](TEST_STATUS.md) for current status.

---

## 🏗 Architecture

```
Kosmosic-Orbiton/
├── kosmosic_orbiton.py          # Main entry point
├── neuro_link_intel.py          # Intelligence / NLP module
├── CHANGELOG.md                 # Version history
├── PHILOSOPHY.md                # Why Orbiton exists
├── ROADMAP.md                   # Where we are going
├── CONTRIBUTING.md              # How to contribute
├── CONTRIBUTORS.md              # Who built this
├── TEST_STATUS.md               # Per-test CI status
├── TESTS.md                     # Test architecture docs
├── WORKFLOWS.md                 # CI/CD configuration docs
├── tests/                       # Full pytest suite
│   ├── conftest.py              # Shared fixtures
│   ├── core_logic/              # Intent & pattern tests
│   ├── url_engine/              # URL generation tests
│   ├── compute/                 # Math & security tests
│   ├── launch/                  # File & project tests
│   ├── system/                  # Status & time tests
│   └── integration/             # End-to-end flow tests
└── .github/workflows/           # CI/CD definitions
```

---

## ⚙️ Configuration

Edit the `CONFIG` dict in `kosmosic_orbiton.py`:

| Key | Default | Description |
|-----|---------|-------------|
| `wake_word` | `"tokyo"` | Voice wake trigger |
| `voice` | `"en-US-AriaNeural"` | TTS voice profile |
| `audio_timeout` | `8` | Seconds to listen |
| `phrase_limit` | `6` | Max phrase duration |
| `memory_file` | `~/.neuro_link_memory.json` | User memory store |

---

## 🖥 Platform Support

| OS | Status | Notes |
|----|--------|-------|
| Windows | ✅ Full | File Explorer, PowerShell TTS, VS Code projects |
| macOS | ✅ Full | `open`, `say`, `afplay` |
| Linux | ✅ Partial | `xdg-open`, `spd-say`, best-effort headphone detection |

---

## 📚 Documentation

| Doc | What it covers |
|-----|---------------|
| [PHILOSOPHY.md](PHILOSOPHY.md) | Why Orbiton exists, privacy stance, open source philosophy |
| [ROADMAP.md](ROADMAP.md) | Model classes (Tokyo → Genesis → Micron → Singularity), features, company vision |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute, testing rules, adding commands, code style |
| [CONTRIBUTORS.md](CONTRIBUTORS.md) | List of contributors |
| [TEST_STATUS.md](TEST_STATUS.md) | Per-test CI status and badges |
| [TESTS.md](TESTS.md) | Test architecture, directory structure, writing new tests |
| [WORKFLOWS.md](WORKFLOWS.md) | CI/CD workflow configuration and troubleshooting |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🏢 About Kosmosic

**Kosmosic** is the company behind Orbiton. We build tools that make your workspace smarter, faster, and slightly more judgmental.

> *"Your ancestors built empires. You can't even close 3 Chrome tabs."* — Orbiton

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0**.

See [LICENSE](LICENSE) for the full text, or visit [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).

> Orbiton is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

---

© 2026 Kosmosic
