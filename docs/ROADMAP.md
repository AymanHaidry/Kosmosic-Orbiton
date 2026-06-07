# Orbiton Roadmap

> *"We put the world around your head."* — Current status: **Tokyo-class** (Generation 1)

---

## Model Classes & Generations

Orbiton evolves through **generations**, each named after a model class. Each generation represents a major era of intelligence, capability, and integration depth.

| Generation | Class | Description | Version | Status |
|------------|-------|-------------|---------|--------|
| 1 | **Tokyo** | Basic reasoning, voice commands, web search, file management, aviation tools, toxic motivation. | `1.x.x` | **Current** |
| 2 | **Odyssey** | Large-scale growth. Advanced reasoning, local LLM integration, long-term memory, personalization engine. | `2.x.x` | Planned |
| 3 | **Genesis** | Agentic behavior. Long-running tasks, predictive execution, multi-step workflows, scraper living on your PC. | `3.x.x` | Planned |
| 4 | **Micron** | Lite version. All core functionality, stripped of heavy dependencies, for older hardware or minimal installs. | `4.x.x` | Planned (ROI-dependent) |
| 5 | **Aphrodite** | Expansion beyond the original vision. IoT integration, multi-language support, various voices, wake word customization. | `5.x.x` | Planned |
| 6 | **Singularity** | Full autonomy. Multi-device ecosystem, predictive everything, self-maintenance, multi-device continuity. | `6.x.x` | Vision |
| 7 | **Utopia** | Final evolution. The absolute top. Orbiton becomes the second user of your computer. | `7.x.x` | Final Vision |

See [VERSIONS.md](VERSIONS.md) for the full versioning system and release rules.

---

## Generation 1 — Tokyo (Current)

### What Works Now
- Voice wake word ("Tokyo") and natural language command parsing
- Web search, YouTube search, Google Maps, Street View
- Weather, airport search, flight tracking (FlightRadar24), METAR/TAF
- File/folder opening and navigation
- VS Code project launcher
- Python script runner
- Clipboard search
- Calculator and math expressions
- Exam mode (calculator + Desmos + notepad)
- Toxic motivation engine
- Session status and time
- User memory (learns facts about you)
- Local knowledge base (moon phases, aviation facts, space facts)
- Wikimedia scraping with caching
- Cross-platform: Windows, macOS, Linux

### Known Bugs
1. **Self-listening on PC.** Orbiton hears its own TTS output and sometimes triggers a random intel response.
2. **"Help" command unresponsive.** Saying "help" does not always execute the help handler.
3. **Exam mode vs "exam board" NLP.** "Exam board" (two words) falls through to generic search instead of triggering exam mode.
4. **Linux headphone auto-detect is best-effort only.**
5. **Edge TTS requires internet.** Offline fallback to system TTS is silent if edge-tts is installed but unreachable.
6. **Hardcoded Windows project paths** in `PROJECTS` dict.

---

## Generation 2 — Odyssey (Planned)

Large-scale growth. Advanced reasoning and memory.

### Intelligence
- **Local LLM integration** (Ollama, llama.cpp, or similar) for offline reasoning
- **Cloud LLM fallback** for complex queries when local is insufficient
- **Long-term memory** that persists across sessions and builds a user model
- **Personalization engine** that adapts commands, roasts, and suggestions to the user
- **Scraper living on your PC** that gathers info and converts to JSON for the main `.py` file
- **OTA intel updates** — download new knowledge bases without updating the whole app

### Hardware & Integration
- **More headset support** beyond JBL — Sony, Bose, AirPods, generic Bluetooth
- **Wake word customization** — choose your own wake word
- **Multiple voices** — switch between TTS voices
- **Multi-language support** — NLP normalization for other languages

---

## Generation 3 — Genesis (Planned)

Agentic behavior and true automation.

### Agentic Tasks
- **Long-running tasks** — "remind me in 2 hours," "download this when WiFi is back"
- **Predictive execution** — suggest commands based on time of day, habits, calendar
- **Multi-step workflows** — "study mode" opens Kosmosic, sets timer, enables Do Not Disturb
- **Talk to others** — share commands or intel files between Orbiton instances

### PC Management
- **System info** — CPU/RAM monitoring, disk usage, process management
- **Kill processes** — "kill Chrome" or "close Notepad"
- **Restart services** — manage system services via voice

---

## Generation 4 — Micron (Planned — ROI-Dependent)

A lightweight Orbiton for constrained environments. Only built if Odyssey and Genesis prove the concept and there is demand for a minimal version.

- Remove rich/console dependency (plain text only)
- Remove edge-tts dependency (system TTS only)
- Strip built-in intel databases (load on demand)
- Reduce wake word sensitivity for faster response
- Target: Raspberry Pi, old laptops, minimal VMs, embedded systems

---

## Generation 5 — Aphrodite (Planned)

Expansion beyond the original vision.

### Communication
- **Send emails** via voice command
- **Place calls** using system dialer or VoIP integration
- **Calendar management** — create events, check schedule, set reminders

### IoT & Smart Home
- **Control lights** — "turn off bedroom lights"
- **Thermostat control** — "set temperature to 22"
- **Smart plugs** — "turn on the coffee maker"
- **Home hub integration** — manage all household Orbiton instances

### Personalization
- **Wake word customization** — any word, not just "Tokyo"
- **Voice selection** — multiple TTS voices to choose from
- **Language packs** — full NLP support for other languages

---

## Generation 6 — Singularity (Vision)

Full autonomy. The second user of your computer.

### Ecosystem
- **Wearables**: Smartwatch companion, always-listening earbud firmware
- **Smart glasses**: HUD overlay with Orbiton status and commands
- **Single-board computers**: Dedicated Orbiton appliance (Pi, Jetson, etc.)
- **Home integration**: Central hub that manages all household Orbiton instances

### Autonomy
- **Replaces bloatware AIs** — no more Cortana, Siri, or generic assistants
- **Predictive everything** — knows what you need before you ask
- **Self-maintenance** — updates intel, cleans cache, optimizes itself
- **Multi-device continuity** — start a command on PC, finish on watch

---

## Generation 7 — Utopia (Final Vision)

The absolute top. Orbiton becomes an ecosystem.

- **Global-scale platform evolution** — not just your PC, but every device you own
- **Interconnected ecosystem** — all your Orbiton instances talk to each other
- **True ambient intelligence** — invisible, proactive, always helpful
- **The second user of your computer** — it knows your workflow better than you do

---

## Pre-2.0 Checklist (Odyssey Release)

Before we call it Generation 2, these must be true:

- [ ] Local LLM integration working offline
- [ ] Long-term memory persists across sessions
- [ ] Personalization engine adapts to user habits
- [ ] Test suite passes 100% on all three OSes
- [ ] Config system replaces hardcoded values
- [ ] Auth system (online accounts) for multi-user support
- [ ] Website for downloads, docs, and intel sharing
- [ ] Self-listening bug resolved
- [ ] Help command bug resolved
- [ ] Documentation complete

---

## What We Are NOT Doing (Yet)

- **Mobile app** — keeps the terminal feel and aesthetic alive. PC users did not have Galaxy AI or Gemini. That is our focus.
- **Cloud dependency** — everything possible stays local. Cloud LLM is a fallback, not a requirement.
- **Generic consumer product** — Orbiton is built for people who care about their tools.

---

## Technical Debt to Clear

- [ ] Config file system (JSON/YAML) instead of hardcoded `CONFIG` dict
- [ ] Auth system (online accounts) for multi-user machines
- [ ] Website for OTA intel updates and community sharing
- [ ] Standardize subprocess usage across all platforms
- [ ] Plugin architecture for third-party commands
- [ ] Better error recovery and logging

---

## Why This Might Stop

Honest boundaries:

- **10th board exams** — school comes first
- **Normal exams** — academic priorities
- **Interest shifts** — something cooler appears
- **Gets boring** — no visible progress-to-reward conversion
- **Discovers something more interesting** — it happens

If any of these happen, the repo stays open. Fork it. Improve it. Make it yours.

---

## The Company Vision

Kosmosic is planned to scale beyond a solo project. The goal is a company that builds tools for people who want **real** control over their digital environment — not packaged slopware. The terminal aesthetic, the voice-first design, and the local-first privacy stance are not temporary. They are the foundation.

Orbiton is Generation 1. There are 6 more to go.

---

> *"The Doha apartment is not paying for itself. Get back to work, peasant."* — Orbiton, pushing you toward the future
