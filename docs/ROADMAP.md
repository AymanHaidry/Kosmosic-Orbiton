# Orbiton Roadmap

> *"We put the world around your head."* — Current status: **Tokyo-class**

---

## Model Classes

Orbiton releases are organized by **class**, not version number. Each class represents a tier of intelligence, capability, and integration depth.

| Class | Tier | Description | Status |
|---|---|---|---|
| **Tokyo-class** | 1st | Basic reasoning, voice commands, web search, file management, aviation tools, toxic motivation. | **Current** |
| **Genesis-class** | 2nd | Advanced reasoning, local LLM integration, long-term memory, personalization engine, agentic tasks. | Planned |
| **Micron-class** | 3rd | Lite version. All core functionality, stripped of heavy dependencies, for older hardware or minimal installs. | Planned (ROI-dependent) |
| **Singularity-class** | Final | Full autonomy, multi-device ecosystem, predictive execution, hardware integration. | Vision |

---

## Tokyo-class (Current)

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
- Local knowledge base (constellations, moon phases, aviation facts, space facts)
- Wikipedia scraper with caching
- Cross-platform: Windows, macOS, Linux

### Known Bugs
1. **Self-listening on PC.** Orbiton hears its own TTS output and sometimes triggers a random intel response.
2. **"Help" command unresponsive.** Saying "help" does not always execute the help handler — likely a misheard wake word or NLP routing issue.
3. **Exam mode vs "exam board" NLP gap.** "Exam board" (two words) falls through to generic search instead of triggering exam mode.
4. **Linux headphone auto-detect is best-effort only.**
5. **Edge TTS requires internet.** Offline fallback to system TTS is silent if edge-tts is installed but unreachable.
6. **Hardcoded Windows project paths** in `PROJECTS` dict.

---

## Genesis-class (Planned)

Advanced reasoning and true agentic behavior.

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
- **IoT integration** — control lights, thermostats, smart plugs via voice
- **PC management** — system info, CPU/RAM monitoring, kill processes, restart services
- **Talk to others** — share commands or intel files between Orbiton instances

### Agentic Tasks
- **Long-running tasks** — "remind me in 2 hours," "download this when WiFi is back"
- **Predictive execution** — suggest commands based on time of day, habits, calendar
- **Multi-step workflows** — "study mode" opens Kosmosic, sets timer, enables Do Not Disturb

### Communication (Post-Genesis / ~v4.0)
- **Send emails** via voice command
- **Place calls** using system dialer or VoIP integration
- **Calendar management** — create events, check schedule, set reminders

---

## Micron-class (Planned — ROI-Dependent)

A lightweight Orbiton for constrained environments. Only built if Genesis proves the concept and there is demand for a minimal version.

- Remove rich/console dependency (plain text only)
- Remove edge-tts dependency (system TTS only)
- Strip built-in intel databases (load on demand)
- Reduce wake word sensitivity for faster response
- Target: Raspberry Pi, old laptops, minimal VMs, embedded systems

---

## Singularity-class (Final Vision)

The absolute top. Orbiton becomes the second user of your computer.

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

## Pre-1.0 Checklist

Before we call it v1.0, these must be true:

- [ ] All basic commands polished and bug-free
- [ ] Test suite passes 100% on all three OSes
- [ ] Config system replaces hardcoded values
- [ ] Auth system (online accounts) for multi-user support
- [ ] Website for downloads, docs, and intel sharing
- [ ] Self-listening bug resolved
- [ ] Help command bug resolved
- [ ] Documentation complete (README, PHILOSOPHY, CONTRIBUTING, API docs)

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

Orbiton is planned to scale beyond a solo project. The goal is a company that builds tools for people who want **real** control over their digital environment — not packaged slopware. The terminal aesthetic, the voice-first design, and the local-first privacy stance are not temporary. They are the foundation.

---

> *"The Doha apartment is not paying for itself. Get back to work, peasant."* — Orbiton, pushing you toward the future
