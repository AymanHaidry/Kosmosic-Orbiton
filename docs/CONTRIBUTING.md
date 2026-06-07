# Contributing to Kosmosic Orbiton

Thanks for checking out Orbiton. Whether you are fixing a bug, adding a command, or just cleaning up code, this guide will get you started.

> **Who is this for?** Anyone. Grade 10 student building their first project? Welcome. Senior dev with opinions? Also welcome. Just make it work and make it fit.

---

## Table of Contents

1. [Project Philosophy](#project-philosophy)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Quality Checklist](#quality-checklist)
5. [Testing Requirements](#testing-requirements)
6. [Adding a New Command](#adding-a-new-command)
7. [Code Style](#code-style)
8. [What Will Get Rejected](#what-will-get-rejected)
9. [Need Help?](#need-help)

---

## Project Philosophy

Orbiton is a **voice-first command terminal** built for people who want the world around their head without touching a keyboard.

**Core principles:**
- **Voice is the primary interface.** Everything should be speakable, natural, and forgiving of sloppy speech.
- **Aviation, space, and study are first-class citizens.** METAR lookups, flight tracking, and exam mode are not afterthoughts.
- **Toxic motivation is accountability.** The roasts are harsh on purpose. If you add new ones, keep the energy.
- **It should feel like an Apple product booted into a terminal.** Clean output, minimal clutter, no noise.
- **Cross-platform matters.** Windows, macOS, and Linux should all work. If you only test one, say so.

**What we are NOT:**
- A general-purpose chatbot (use ChatGPT for that).
- A GUI application (keep it terminal + voice).
- A cloud service. Your data lives in a local `_.pycache_` folder. Not our servers. Not Microsoft's. Yours.
- Ads, paywalls, or "vibecoded ultra 2050 spaceship neon purple gamer aesthetic." If it looks like it belongs on a Fortnite skin, it does not belong in Orbiton.
- *Project Hail Mary*. Do not ask.

**Read the full philosophy:** [PHILOSOPHY.md](PHILOSOPHY.md)

---

## Getting Started

### Prerequisites

- Python 3.10+
- A microphone (for voice testing)
- Git

### Setup

```bash
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmic-Orbiton
pip install -r requirements.txt   # or: pip install speechrecognition rich edge-tts
```

### Run it locally

```bash
python kosmosic_orbiton.py
```

Say **"Tokyo"** to wake it up, then try any command.

---

## How to Contribute

### If you are Ayman (project owner)

Push directly to `main`. You own the repo. Just do not break it.

### If you are anyone else

1. **Fork the repo** (or ask for collaborator access if you are a regular).
2. **Create a branch:** `git checkout -b your-feature-name`
3. **Make your changes.**
4. **Test everything.** See [Testing Requirements](#testing-requirements).
5. **Open a Pull Request.** No issue required, but you can open one if you want to discuss first.
6. **Wait for review.** If it works and aligns with the philosophy, it gets merged.

> **Note:** Issues are optional. If you found a bug and know how to fix it, just send the PR. If you are not sure, open an issue and we will talk.

---

## Quality Checklist

Before you open a PR, make sure you can check every box:

- [ ] **It works on your machine.** Test the actual command, not just the code path.
- [ ] **You documented any errors you hit** and how you fixed them (screenshot + explanation).
- [ ] **You did not create new bugs** in existing commands.
- [ ] **You added tests** if you added something new. See [Testing Requirements](#testing-requirements).
- [ ] **Your change aligns with the philosophy.** Does it feel like Orbiton?
- [ ] **You tested on your OS.** If you only tested Windows, say that in the PR.

---

## Testing Requirements

### For code changes

Run the full test suite:

```bash
pytest tests/ -v
```

All tests must pass. If you added a new command, add tests for it:

| What you added | Test file to create/modify |
|---|---|
| New URL-opening command | `tests/url_engine/test_<command>_urls.py` |
| New intent/parser pattern | `tests/core_logic/test_intent_parser.py` |
| New file/folder behavior | `tests/launch/test_<feature>.py` |
| New math/utility | `tests/compute/test_<feature>.py` |
| New system feature | `tests/system/test_<feature>.py` |
| End-to-end flow | `tests/integration/test_<feature>_flow.py` |

### For voice commands

Voice commands are hard to unit test. If you add or modify one, **record a screen capture** showing:

1. You saying the wake word ("Tokyo").
2. You giving the command.
3. Orbiton responding correctly.

Upload the video to the PR description or link it (YouTube unlisted, Google Drive, etc.).

### Bug fixes

If you fixed a bug:
- Add a test that would have caught the bug.
- Include a screenshot of the error **before** your fix.
- Include proof it is fixed **after**.

---

## Adding a New Command

Want to add "translate hello to French" or "set a timer for 5 minutes"? Here is the checklist:

### 1. Add the handler in `kosmosic_orbiton.py`

```python
def handle_translate(self, query: str):
    url = f"https://translate.google.com/?sl=auto&tl=en&text={quote(query)}"
    self.open_chrome(url)
    msg = f"Translating: {query}"
    self.ui.show_success(msg)
    self.speak(msg)
```

### 2. Add the intent pattern in `IntentParser.PATTERNS`

```python
(r"^(?:translate|translation|what does)\s+(.+)", "translate"),
```

### 3. Add NLP support in `neuro_link_intel.py` (optional but recommended)

If the command is commonly misheard, add homophones:

```python
"translait": "translate",
"translete": "translate",
```

### 4. Add it to the help table

In `ALL_COMMANDS`:

```python
("Translate", "translate <text>", "Google Translate anything"),
```

### 5. Add tests

- `tests/url_engine/test_translate_urls.py` — verify URL generation.
- `tests/core_logic/test_intent_parser.py` — verify intent recognition.
- `tests/integration/test_translate_flow.py` — verify end-to-end flow.

### 6. Update this doc if needed

If your command introduces a new pattern others should follow, add it here.

---

## Code Style

We do not enforce a formatter, but keep it consistent with what is already there:

- **4 spaces for indentation.** No tabs.
- **Type hints encouraged** but not required.
- **Docstrings for public methods.** One line is fine.
- **Match the existing naming.** `handle_*` for command methods, `test_*` for tests.
- **No trailing whitespace.**

If you are unsure, run:

```bash
python -m py_compile kosmosic_orbiton.py neuro_link_intel.py
```

If it compiles, you are probably fine.

---

## What Will Get Rejected

- **Code that breaks existing commands.** If "search python" stops working, it is not getting merged.
- **Features that require heavy GUI frameworks.** Orbiton is voice + terminal. No Tkinter, no PyQt.
- **Features that phone home or track users.** Privacy is assumed.
- **AI-generated code without disclosure.** If you used Copilot/ChatGPT/etc to write significant chunks, say so in the PR. We will not reject it automatically, but we need to know.
- **References to *Project Hail Mary*.** Just do not.

---

## Known Issues & Future Work

These are things we know about and are not fixing right now. If you want to tackle one, open a PR:

- **Self-listening on PC.** Orbiton hears its own TTS output and sometimes triggers a random intel response.
- **"Help" command unresponsive.** Saying "help" does not always execute the help handler.
- **Exam mode vs "exam board" NLP.** The regex catches "exambored" but "exam board" (two words) still falls through to NLP. Could be tighter.
- **No Linux headphone auto-detect.** `get_connected_headphones()` works on Windows and macOS but Linux support is best-effort.
- **Edge TTS requires internet.** Fallback to system TTS is silent if edge-tts is installed but offline.
- **Hardcoded Windows project paths** in `PROJECTS` dict.

**See the full roadmap:** [ROADMAP.md](ROADMAP.md)

---

## Need Help?

- **Open an issue:** For bugs, feature requests, or "how do I..." questions.
- **Check the code:** The docstrings are actually decent. Start with `kosmosic_orbiton.py` -> `CommandEngine`.
- **Read the roadmap:** If you want to know where the project is headed.

---

## Contributors

| Name | Contribution |
|---|---|
| Ayman Haidry | Creator, everything |
| *Your name here* | Send a PR |

---

> *"Your ancestors built empires. You cannot even close 3 Chrome tabs."* — Orbiton
