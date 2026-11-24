# Architecture Decisions — Orbiton (Kosmosic)

This document records all major architectural decisions made during the development of Orbiton. Each entry follows the ADR (Architecture Decision Record) format.

---

## ADR-001: Python as the Core Runtime

**Date:** 2026-06-06  
**Status:** Accepted  
**Version:** v0.1.0

### Decision
Orbiton is built entirely in Python 3.11+.

### Context
The project needed a language that supports rapid prototyping, has mature libraries for speech recognition and TTS, and runs cross-platform without compilation.

### Alternatives Considered
- **Node.js** — Good async support but weaker speech/audio ecosystem
- **Go** — Fast but no mature speech recognition bindings
- **C++** — Maximum performance but prohibitive development overhead

### Rationale
Python has `SpeechRecognition`, `edge-tts`, `rich`, and `pytest` — all mature, well-maintained libraries that cover every requirement. Cross-platform support (Windows, macOS, Linux) is first-class.

### Tradeoffs
- ✅ Rapid development, large ecosystem
- ✅ Easy for contributors to onboard
- ⚠️ Slower startup than compiled languages
- ⚠️ GIL limits true parallelism (mitigated with `threading` + `asyncio`)

---

## ADR-002: Google Web Speech API for Voice Recognition

**Date:** 2026-06-06  
**Status:** Accepted  
**Version:** v0.2.0

### Decision
Use `SpeechRecognition` library with Google Web Speech API as the default recognition backend.

### Context
Orbiton needs accurate, low-latency voice recognition without requiring local model downloads.

### Alternatives Considered
- **Whisper (OpenAI)** — High accuracy but requires local GPU/CPU model (~1.5GB)
- **Vosk** — Offline, lightweight, but lower accuracy
- **Azure Speech** — Paid, requires API key setup
- **CMU Sphinx** — Offline but outdated and low accuracy

### Rationale
Google Web Speech API is free for reasonable usage, requires no API key, and delivers excellent accuracy for English commands. The `SpeechRecognition` library abstracts the backend, making it easy to swap in the future.

### Tradeoffs
- ✅ No API key required, free tier sufficient
- ✅ High accuracy for English
- ⚠️ Requires internet connection
- ⚠️ Privacy: audio sent to Google servers
- ⚠️ Rate limits may apply at scale

---

## ADR-003: Microsoft Edge TTS for Text-to-Speech

**Date:** 2026-06-06  
**Status:** Accepted  
**Version:** v0.2.0

### Decision
Use `edge-tts` (Microsoft Edge neural TTS) as the primary voice output engine.

### Context
Orbiton needed a high-quality, natural-sounding TTS voice that works cross-platform without paid API keys.

### Alternatives Considered
- **pyttsx3** — Offline, but robotic voice quality
- **Google Cloud TTS** — Excellent quality but requires billing
- **Amazon Polly** — Excellent quality but requires AWS account
- **System TTS** (`say`, `spd-say`, PowerShell) — Available offline but inconsistent quality

### Rationale
`edge-tts` provides neural-quality voices (en-US-AriaNeural) for free, with no API key. It uses the same backend as Microsoft Edge browser's read-aloud feature.

### Tradeoffs
- ✅ Neural quality voice, free
- ✅ No API key required
- ⚠️ Requires internet connection
- ⚠️ Depends on Microsoft's unofficial API (may break without notice)
- ✅ Graceful fallback to system TTS when offline

---

## ADR-004: Wake Word "TOKYO" Design

**Date:** 2026-06-06  
**Status:** Accepted  
**Version:** v0.3.0

### Decision
Use "TOKYO" as the default wake word, detected via substring matching in the recognized speech.

### Context
Orbiton needed a distinctive wake word that is unlikely to appear in normal conversation and is easy to pronounce across accents.

### Alternatives Considered
- **"Hey Orbiton"** — Too long, recognition unreliable
- **"Orbiton"** — Unique but hard to pronounce
- **Custom hotword detection (Porcupine)** — Accurate but requires paid license
- **"Computer"** — Too generic, false positives

### Rationale
"TOKYO" is short, distinctive, phonetically clear, and aligns with the Tokyo-class product naming. Substring matching is simple and reliable for a single-word trigger.

### Tradeoffs
- ✅ Simple implementation, no extra dependencies
- ✅ Distinctive, low false-positive rate
- ⚠️ Not a true hotword detector (requires active listening loop)
- ⚠️ Wake word customization planned for future release

---

## ADR-005: Single-file Intelligence Module (Superseded)

**Date:** 2026-06-07  
**Status:** Superseded by ADR-011  
**Version:** v0.4.0

### Decision
Extract all NLP, knowledge lookup, and math normalization logic into a dedicated `neuro_link_intel.py` module, separate from the main `kosmosic_orbiton.py` entry point.

### Context
As Orbiton's intelligence features grew (NLP normalization, homophone correction, Wikimedia integration, math parsing), the main file became unwieldy. Testing individual intelligence components was difficult.

### Alternatives Considered
- **Keep everything in `kosmosic_orbiton.py`** — Simpler but unscalable
- **Full package structure (`orbiton/` directory)** — More Pythonic but over-engineered for current scale
- **Plugin system** — Flexible but complex

### Rationale
A single companion module provides clean separation of concerns without the overhead of a full package. It can be imported independently for testing and is easy for contributors to understand.

### Tradeoffs
- ✅ Clean separation of concerns
- ✅ Independently testable
- ✅ Easy to extend with new intelligence features
- ⚠️ Circular import risk if not carefully managed
- ⚠️ Not a full plugin architecture (planned for Genesis-class)

---

## ADR-006: `safe_eval` for Math Expression Evaluation

**Date:** 2026-06-07  
**Status:** Accepted  
**Version:** v0.6.2

### Decision
Replace raw `eval()` with a bounded AST interpreter in `MathNormalizer.safe_eval()`, combined with `MathNormalizer.normalize()` to convert spoken math into a restricted expression tree.

### Context
The original `calculate` command used `eval()` directly on user speech input, creating a code injection vulnerability. Spoken math ("two times two", "three squared") also failed to parse.

### Alternatives Considered
- **`ast.literal_eval()`** — Safe but only handles literals, not expressions
- **`sympy`** — Full symbolic math but heavy dependency
- **`numexpr`** — Fast but adds a dependency
- **Custom parser** — Maximum control but high implementation cost

### Rationale
A bounded AST interpreter accepts numeric literals, arithmetic operators, `math.pi`/`math.e`, and explicitly permitted functions (`sqrt`, `cbrt`, `factorial`, `abs`, and `round`). Expression length, AST node count, exponent size, factorial input, and result magnitude are bounded. `MathNormalizer` handles the spoken-to-symbolic conversion layer.

### Tradeoffs
- ✅ Eliminates code injection risk
- ✅ Handles spoken math naturally
- ✅ No additional dependencies
- ⚠️ Limited to arithmetic (no symbolic algebra)
- ⚠️ Edge cases in spoken math normalization may still exist

---

## ADR-007: Standalone Troubleshooter Tool (`troubleshooter.py`)

**Date:** 2026-06-08  
**Status:** Accepted  
**Version:** v0.7.0

### Decision
Ship a standalone `troubleshooter.py` interactive diagnostic tool as a separate script, not integrated into the main Orbiton runtime.

### Context
User support requests were dominated by setup issues (missing dependencies, microphone problems, TTS failures). A guided diagnostic tool would reduce support burden and improve onboarding.

### Alternatives Considered
- **Integrate into `kosmosic_orbiton.py`** — Convenient but bloats the main runtime
- **Web-based diagnostic** — Accessible but requires a server
- **Shell script** — Cross-platform issues
- **Separate `diagnostics/` package** — Better architecture but over-engineered for v0.7

### Rationale
A standalone script with zero dependencies beyond the Python standard library ensures it works even when Orbiton's dependencies are broken. It can diagnose the very failures that would prevent the main app from running.

### Tradeoffs
- ✅ Works even when dependencies are missing
- ✅ No dependency on `rich` or other packages
- ✅ Easy to run: `python troubleshooter.py`
- ⚠️ Bandit flags `subprocess` usage (intentional, local-only tool — see issue #60)
- ⚠️ Duplicates some logic from main app (acceptable for a diagnostic tool)
- 🔜 Planned refactor into `diagnostics/` module for v0.8.0

---

## ADR-008: Test Suite Architecture (Category-Based CI)

**Date:** 2026-06-07  
**Status:** Accepted  
**Version:** v0.6.0

### Decision
Organize tests into 7 categories (`core_logic`, `url_engine`, `compute`, `launch`, `system`, `integration`, `troubleshooter`), each running as a separate CI job.

### Context
A flat test directory made it hard to identify which area of the codebase was failing. CI runs were slow and failures were hard to triage.

### Alternatives Considered
- **Single test file** — Simple but unscalable
- **Test by module** — Mirrors source structure but mixes concerns
- **BDD (Behave/pytest-bdd)** — Expressive but adds complexity

### Rationale
Category-based organization mirrors the functional areas of Orbiton (voice commands, URL generation, math, file operations, etc.). Separate CI jobs provide fast, parallel feedback and clear failure attribution.

### Tradeoffs
- ✅ Fast parallel CI
- ✅ Clear failure attribution
- ✅ Easy to add new categories
- ⚠️ Some test duplication across categories
- ⚠️ `conftest.py` shared fixtures must be carefully managed

---

## ADR-009: Documentation in `docs/` Subdirectory

**Date:** 2026-06-07  
**Status:** Accepted  
**Version:** v0.4.0

### Decision
Store all extended documentation in a `docs/` subdirectory, with key files (`README.md`, `SECURITY.md`, `LICENSE.md`, `MANUAL.md`, `TROUBLESHOOT.md`) duplicated at the root for GitHub discoverability.

### Context
GitHub surfaces certain files (README, SECURITY, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT) from the root. Extended documentation belongs in `docs/` for organization.

### Alternatives Considered
- **All docs at root** — Simple but clutters the root directory
- **GitHub Wiki** — Separate from code, harder to version
- **Docusaurus/MkDocs site** — Professional but heavy overhead for current scale

### Rationale
Dual placement (root + docs/) satisfies both GitHub's automatic file detection and organized documentation browsing. The website (`theorbiton.vercel.app`) serves as the public-facing docs portal.

### Tradeoffs
- ✅ GitHub auto-detects SECURITY.md, LICENSE.md, CONTRIBUTING.md
- ✅ Organized docs/ directory for extended content
- ⚠️ Some files duplicated (README, MANUAL, TROUBLESHOOT) — must be kept in sync
- ⚠️ Sync discipline required on every release

---

## ADR-010: Model Class Naming Convention (Tokyo → Singularity)

**Date:** 2026-06-06  
**Status:** Accepted  
**Version:** v0.1.0

### Decision
Name Orbiton release generations after cities/concepts: Tokyo-class (v0.x), Odyssey-class (v1.x), Genesis-class (v2.x), Micron-class (v3.x), Aphrodite-class (v4.x), Singularity-class (v5.x), Utopia-class (v6.x).

### Context
Product naming creates brand identity and communicates the scope of each generation to users and contributors.

### Rationale
City/concept names are memorable, internationally recognizable, and convey a sense of progression. The naming mirrors the ambition of each generation (Tokyo = foundation, Genesis = AI integration, Singularity = autonomous intelligence).

### Tradeoffs
- ✅ Memorable, brand-building
- ✅ Clear generational progression
- ⚠️ Names must be chosen carefully to avoid cultural insensitivity
- ⚠️ Version numbers (v0.x, v1.x) must align with class names in all docs

---

*Last updated: 2026-11-24 by Orbiton Workflow Agent (scheduled health scan)*  
*For the full roadmap, see [ROADMAP.md](ROADMAP.md)*


---

## ADR-011: Focused Stag Package Modules

**Date:** 2026-11-24  
**Status:** Accepted  
**Version:** Cleanup Drive

### Decision
Split NLP, safe arithmetic, and online knowledge routing into separately testable modules under `stag/`. Remove the old `neuro_link_intel.py` module and its local static/custom knowledge database.

### Rationale
The former file combined unrelated concerns and created a misleading impression that general knowledge was preloaded. Focused modules improve testability and make the live-research provider easier to replace.


---

## ADR-012: Modular Application Package

**Date:** 2026-11-24  
**Status:** Accepted  
**Version:** Cleanup Drive

### Decision
Move application responsibilities into focused modules under `stag/`: app lifecycle, commands, configuration, device integrations, intelligence, memory, NLP, parsing, terminal UI, and voice output. Keep `kosmosic_orbiton.py` as a compatibility launcher and expose an installable `orbiton` console command.

### Rationale
The previous entry point mixed nearly every concern in one file. A package makes responsibilities visible, lets contributors locate code without searching a monolith, and provides a stable public launch command without forcing a breaking change on existing scripts.

### Consequences
- New code should import from `stag.*`.
- The recommended launch commands are `orbiton` or `python -m stag`.
- The compatibility launcher remains until the separate rebrand work decides its final public name.
