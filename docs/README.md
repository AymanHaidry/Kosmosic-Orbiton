![Core Logic](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/core-logic.yml/badge.svg)
![URL Engine](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/url-engine.yml/badge.svg)
![Compute](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/compute.yml/badge.svg)
![Launch](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/launch.yml/badge.svg)
![System](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/system.yml/badge.svg)
![Integration](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/integration.yml/badge.svg)
![Pylint](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/pylint.yml/badge.svg)
# 🎧 Orbiton — Voice Command Terminal

> *"We put the world around your head."*


**Company:** Kosmosic  
**Product:** Orbiton  
**Wake Word:** TOKYO

Orbiton is a Python-powered desktop voice assistant that turns your headset into a wireless command terminal. Launch apps, search the web, open files, manage projects, and automate everyday tasks using natural voice commands.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmic-Orbiton

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

---

## 🎤 Voice Commands

| Category | Command | Description |
|----------|---------|-------------|
| 🔍 Search | `search <query>` | Google search |
| 🎥 YouTube | `youtube <query>` | Search YouTube |
| 🧮 Math | `calculate <expr>` | Calculate and speak result |
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
- **Knowledge lookup** — constellations, moon phases, aviation facts
- **Wikimedia scraping** — live Wikipedia/Wiktionary queries
- **Contextual routing** — decides whether to search, calculate, or answer directly

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

See [tests/TESTS.md](tests/TESTS.md) for the full test architecture.

---

## 🏗 Architecture

```
Kosmosic-Orbiton/
├── kosmosic_orbiton.py          # Main entry point
├── neuro_link_intel.py          # Intelligence / NLP module
├── CHANGELOG.md                 # Version history
├── tests/                       # Full pytest suite
│   ├── conftest.py              # Shared fixtures
│   ├── core_logic/              # Intent & pattern tests
│   ├── url_engine/              # URL generation tests
│   ├── compute/                 # Math & security tests
│   ├── launch/                  # File & project tests
│   ├── system/                  # Status & time tests
│   └── integration/             # End-to-end flow tests
└── .github/workflows/           # CI/CD (pylint)
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
| Windows | ✅ Full | File Explorer, PowerShell TTS |
| macOS | ✅ Full | `open`, `say`, `afplay` |
| Linux | ✅ Partial | `xdg-open`, `spd-say` |

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
