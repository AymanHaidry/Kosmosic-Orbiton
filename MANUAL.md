# 📖 THE ORBITON MANUAL
## *The Complete, Exhaustive, No-Bullshit Guide to Mastering Kosmosic Orbiton*

> **Version:** 0.6.2 (Tokyo-class)  
> **Last Updated:** 2026-06-08  
> **Read Time:** ~45 minutes if you are thorough. 5 minutes if you are panicking.  
> **Target Audience:** Everyone. A 3rd grader. A 48-year-old senior dev. A cat walking on a keyboard. If you can read, you can master this.

---

## TABLE OF CONTENTS

1. [What Is Orbiton?](#1-what-is-orbiton)
2. [What You Need Before You Start](#2-what-you-need-before-you-start)
3. [Installation: The Absolute Basics](#3-installation-the-absolute-basics)
4. [Your First Run: The Boot Sequence](#4-your-first-run-the-boot-sequence)
5. [How to Talk to Orbiton](#5-how-to-talk-to-orbiton)
6. [The Complete Command Encyclopedia](#6-the-complete-command-encyclopedia)
7. [Typing Commands (No Microphone)](#7-typing-commands-no-microphone)
8. [The Neuro-Link Intelligence System](#8-the-neuro-link-intelligence-system)
9. [Configuration: Making Orbiton Yours](#9-configuration-making-orbiton-yours)
10. [Files, Folders, and Projects](#10-files-folders-and-projects)
11. [The Memory System](#11-the-memory-system)
12. [Knowledge & Wikipedia Lookup](#12-knowledge--wikipedia-lookup)
13. [Platform-Specific Deep Dive](#13-platform-specific-deep-dive)
14. [Hacking Orbiton: Adding Commands](#14-hacking-orbiton-adding-commands)
15. [Testing & Quality Assurance](#15-testing--quality-assurance)
16. [Troubleshooting Bible](#16-troubleshooting-bible)
17. [Architecture Reference](#17-architecture-reference)
18. [The Roadmap: Where Orbiton Is Going](#18-the-roadmap-where-orbiton-is-going)
19. [Contributing to Orbiton](#19-contributing-to-orbiton)
20. [Glossary of Terms](#20-glossary-of-terms)

---

## 1. What Is Orbiton?

Orbiton is a **Python-powered desktop voice assistant** that turns your computer (and ideally your headset) into a wireless command terminal. You speak, it acts. No cloud. No bloat. No subscriptions.

### The One-Sentence Pitch
> *"We put the world around your head."*

### What It Actually Does
- **Opens stuff** — files, folders, VS Code projects, websites, maps
- **Searches stuff** — Google, YouTube, Wikipedia, flight trackers, weather
- **Calculates stuff** — math expressions, even spoken math like "twenty five divided by five"
- **Roasts you** — a "toxic motivation" engine that insults you into productivity
- **Remembers you** — stores facts about you in a local JSON file
- **Answers questions** — looks up knowledge from Wikipedia and local databases

### What It Is NOT
- It is **not** ChatGPT. It does not chat. It commands.
- It is **not** a GUI app. It lives in your terminal.
- It is **not** a cloud service. Your voice never leaves your machine.
- It is **not** gentle. The roasts are harsh. Deal with it.

### The Philosophy (Why This Exists)
Orbiton was built because the creator wanted a computer that obeys him without breaking flow state. No clicking through menus. No typing the same search query for the hundredth time. Just voice → action.

It is built for:
- Sci-fi people who want their computer to feel like a ship console
- Students who need to study but get distracted
- People who want to multitask (voice command while hands stay on keyboard)
- People who are tired of slopware and bloatware

**Privacy stance:** Local. Local. Local. Your data lives in `~/.neuro_link_memory.json`, `~/.neuro_link_intel/`, and `~/.neuro_link_wiki_cache/`. Nothing phones home.

---

## 2. What You Need Before You Start

### Hardware
| Component | Requirement | Notes |
|-----------|-------------|-------|
| Computer | Any PC/Mac/Linux box from the last 10 years | It is Python. It is not demanding. |
| Microphone | Built-in laptop mic, USB mic, or headset | A headset is the *native* habitat. |
| Internet | Optional | Only needed for Edge TTS (voice output) and Wikipedia lookups. Core features work offline. |
| Headphones | Recommended | Prevents Orbiton from hearing its own voice (the "self-listening" bug). |

### Software
| Software | Version | Why You Need It |
|----------|---------|-----------------|
| Python | 3.10 or newer | Orbiton is written in Python. |
| Git | Any | To clone the repository. |
| pip | Any | To install Python dependencies. |
| A terminal | Any | Command Prompt, PowerShell, Terminal.app, GNOME Terminal, iTerm2, etc. |
| Chrome (optional) | Any | Orbiton uses Chrome paths to open URLs. If Chrome is missing, it falls back to the default browser. |

### Operating System Support
| OS | Status | What Works | What Is Janky |
|----|--------|------------|---------------|
| **Windows** | ✅ Full Support | File Explorer, PowerShell TTS, VS Code projects, headphone detection | Nothing major |
| **macOS** | ✅ Full Support | `open`, `say`, `afplay`, VS Code projects | Nothing major |
| **Linux** | ⚠️ Partial Support | `xdg-open`, `spd-say`, file navigation | Headphone detection is best-effort. Edge TTS offline fallback is silent. |

---

## 3. Installation: The Absolute Basics

### Step 1: Clone the Repository
Open your terminal and type exactly this:

```bash
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmosic-Orbiton
```

**What this does:** Downloads the code to a folder named `Kosmosic-Orbiton` on your machine and moves you into that folder.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**What this installs:**
- `speech_recognition` — listens to your microphone
- `edge-tts` — neural text-to-speech (makes Orbiton talk back)
- `rich` — pretty terminal colors and tables
- Other standard library stuff (you already have it)

**If `requirements.txt` is missing or fails, install manually:**
```bash
pip install speechrecognition edge-tts rich
```

### Step 3: Verify It Works
```bash
python kosmosic_orbiton.py
```

You should see a minimalist boot sequence:
```
● → Loading → ✓ Ready
```

If you see this, Orbiton is alive. If you see a wall of red errors, jump to [Troubleshooting](#16-troubleshooting-bible).

---

## 4. Your First Run: The Boot Sequence

When you run `python kosmosic_orbiton.py`, here is exactly what happens:

1. **Python starts** and imports the code.
2. **Optional imports load** — it tries to load `rich` (for pretty UI) and `edge-tts` (for voice). If they are missing, it degrades gracefully.
3. **The intelligence module loads** — `neuro_link_intel.py` is imported. NLP, math, and knowledge engines wake up.
4. **The Apple-style boot sequence prints** — `● → Loading → ✓ Ready`
5. **Orbiton begins listening** — it waits for the wake word or typed input.

### The Interface
You will see a terminal. There is no GUI. There are no buttons. There is:
- A prompt where you can type commands
- A voice listener that activates when you say **"TOKYO"**

### Immediate Things to Try
Say out loud (or type):
- `"TOKYO"` — wakes Orbiton up
- `"what time is it"` — tells you the time
- `"motivate me"` — gets roasted
- `"sleep"` — puts Orbiton to sleep
- `"wake"` or `"TOKYO"` — wakes it back up

---

## 5. How to Talk to Orbiton

### The Wake Word: TOKYO
Orbiton is usually **asleep** to save resources and avoid eavesdropping. To wake it:

**Say:** `"Tokyo"` (or `"tokyo"` — case does not matter)

**What happens:**
- Orbiton snaps to attention
- It listens for your next command for up to 8 seconds (configurable)
- It processes what you said
- It executes the command
- It speaks the result (if applicable)
- It goes back to listening for "Tokyo"

### Speaking Tips
- **Speak clearly** but naturally. You do not need to sound like a robot.
- **One command at a time.** Do not say `"Tokyo search python and also open my downloads folder"`. Do one, then the next.
- **Wait for the wake acknowledgment.** After saying "Tokyo", pause slightly, then give your command.
- **Use a headset if possible.** This prevents the "self-listening" bug where Orbiton hears its own voice and gets confused.

### What If Voice Does Not Work?
See [Typing Commands](#7-typing-commands-no-microphone) and [Troubleshooting: Microphone Issues](#16-troubleshooting-bible).

---

## 6. The Complete Command Encyclopedia

This section documents **every single command** Orbiton understands. Each entry includes:
- The exact phrase to say/type
- What it does
- What URL or action it triggers
- Edge cases and variations

---

### 🔍 Search Commands

#### `search <query>`
**Examples:**
- `"search python tutorial"`
- `"search best pizza near me"`
- `"search how to center a div"`

**What it does:** Opens your default browser to a Google search results page for `<query>`.

**URL generated:** `https://www.google.com/search?q=python+tutorial`

**Edge cases:**
- If `<query>` is empty, it opens Google homepage.
- Special characters are URL-encoded automatically.

---

#### `youtube <query>`
**Examples:**
- `"youtube lofi hip hop"`
- `"youtube cockpit landing"`

**What it does:** Opens YouTube search results for `<query>`.

**URL generated:** `https://www.youtube.com/results?search_query=lofi+hip+hop`

---

#### `maps <place>`
**Examples:**
- `"maps times square"`
- `"maps nearest gas station"`

**What it does:** Opens Google Maps centered on `<place>`.

**URL generated:** `https://www.google.com/maps/search/times+square`

---

#### `streetview`
**Example:** `"streetview"`

**What it does:** Drops you into a random amazing place on Earth via Google Street View. Locations include the Taj Mahal, Golden Gate Bridge, Kyoto Bamboo Grove, etc.

**URL generated:** `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=<lat>,<lon>` (randomly selected from 20 locations)

**The 20 locations:**
1. Kyoto, Japan — Arashiyama Bamboo Grove (35.0116, 135.7681)
2. Reykjavik, Iceland — Northern Lights Spot (64.1466, -21.9426)
3. Paris, France — Eiffel Tower (48.8584, 2.2945)
4. Sydney, Australia — Opera House (-33.8568, 151.2153)
5. San Francisco, USA — Golden Gate Bridge (37.8199, -122.4783)
6. Dubai, UAE — Burj Khalifa (25.1972, 55.2744)
7. Stonehenge, UK (51.1788, -1.8262)
8. Agra, India — Taj Mahal (27.1751, 78.0421)
9. Toronto, Canada — CN Tower (43.6426, -79.3871)
10. Moscow, Russia — Red Square (55.7558, 37.6173)
11. Great Wall of China (40.4319, 116.5704)
12. Machu Picchu, Peru (-13.1631, -72.5450)
13. Rome, Italy — Colosseum (41.9028, 12.4964)
14. Stockholm, Sweden — Gamla Stan (59.3293, 18.0686)
15. Singapore — Marina Bay Sands (1.3521, 103.8198)
16. Ottawa, Canada — Parliament (45.4215, -75.6972)
17. Tokyo, Japan — Shibuya Crossing (35.6762, 139.6503)
18. Munich, Germany — Marienplatz (48.1351, 11.5820)
19. Berlin, Germany — Brandenburg Gate (52.5200, 13.4050)
20. Budapest, Hungary — Parliament (47.4979, 19.0402)

---

#### `clipboard [youtube]`
**Examples:**
- `"clipboard"` — searches whatever is currently on your clipboard
- `"clipboard youtube"` — searches your clipboard content specifically on YouTube

**What it does:** Reads your system clipboard and searches it on Google (or YouTube if you add "youtube").

**Platform notes:**
- **Windows:** Uses `pyperclip` or `win32clipboard`.
- **macOS:** Uses `pbpaste`.
- **Linux:** Uses `xclip` or `xsel`.

---

### 🧮 Math Commands

#### `calculate <expression>`
**Examples:**
- `"calculate 25 * 4"`
- `"calculate two times two"`
- `"calculate twenty five divided by five"`
- `"calculate three squared"`
- `"calculate 100 mod 7"`

**What it does:** Evaluates the math expression and speaks the result.

**How it works (the magic):**
1. You speak a math expression.
2. `MathNormalizer` converts spoken words to digits and operators.
3. `safe_eval` runs the math with a strict whitelist (no code injection possible).
4. Orbiton speaks the answer.

**Spoken math supported:**
| Spoken | Becomes |
|--------|---------|
| zero → nineteen | 0 → 19 |
| twenty, thirty, forty... ninety | 20, 30, 40... 90 |
| hundred | 100 |
| thousand | 1000 |
| million | 1000000 |
| times / into / multiplied by / x | `*` |
| divided by / over | `/` |
| plus / add | `+` |
| minus / subtract | `-` |
| to the power of | `**` |
| squared | `**2` |
| cubed | `**3` |
| mod / modulo | `%` |

**Security:** The `safe_eval` function only allows digits, `+ - * / % . ( )` and spaces. Anything else is rejected. You cannot hack Orbiton with `"calculate __import__('os').system('rm -rf /')"`. It will just say "Unsafe characters."

---

### 🌤 Information Commands

#### `weather [city]`
**Examples:**
- `"weather"` (defaults to your local area or a preset)
- `"weather doha"`
- `"weather new york"`

**What it does:** Opens a Google search for `"weather <city>"`.

**URL generated:** `https://www.google.com/search?q=weather+doha`

**NLP support:** You can also say `"what's the weather in doha"` or `"how is the weather in doha"`. The NLP engine extracts the city automatically.

---

#### `airport <city>`
**Example:** `"airport london"`

**What it does:** Searches for airports in the specified city.

**URL generated:** `https://www.google.com/search?q=london+airport`

---

#### `track <flight>`
**Example:** `"track EK215"`

**What it does:** Opens FlightRadar24 to track the specified flight.

**URL generated:** `https://www.flightradar24.com/EK215`

---

#### `metar <icao>`
**Example:** `"metar KJFK"`

**What it does:** Opens AviationWeather.gov for the METAR (aviation weather report) of the given ICAO airport code.

**URL generated:** `https://aviationweather.gov/metar?icao=KJFK`

**What is METAR?** A standardized format for reporting weather information used by pilots. Orbiton is built with aviation DNA.

---

#### `tell me about <topic>`
**Examples:**
- `"tell me about constellations"`
- `"tell me about the moon"`
- `"tell me about black holes"`

**What it does:**
1. Checks local knowledge bases (moon phases, aviation facts, space facts).
2. If not found locally, queries Wikipedia REST API.
3. Caches the result in `~/.neuro_link_wiki_cache/`.
4. Speaks the first ~500 characters of the answer.

---

#### `what time is it`
**Example:** `"what time is it"`

**What it does:** Tells you the current time in 12-hour format.

**NLP support:** Also understands `"current time"`, `"time check"`, `"tell me the time"`, etc.

---

### 📂 File & Project Commands

#### `open <folder or file>`
**Examples:**
- `"open downloads"`
- `"open documents"`
- `"open myfile.txt"`

**What it does:** Opens the specified file or folder in your OS default application.
- **Windows:** Opens in File Explorer.
- **macOS:** Uses `open` command.
- **Linux:** Uses `xdg-open`.

**How it resolves paths:**
1. Checks if it is a known folder alias (downloads, documents, desktop, pictures, videos, music).
2. Checks if it exists relative to your current directory.
3. Checks if it exists in your home directory (`~`).

---

#### `go to <folder>`
**Examples:**
- `"go to downloads"`
- `"go to parent"` (goes up one directory)
- `"go to back"` (goes to previous directory)

**What it does:** Changes Orbiton's internal working directory. This affects where `open` and `run` look for files.

---

#### `open project <name>`
**Examples:**
- `"open project hex link"`
- `"open project runway objects"`
- `"open project udestini"`

**What it does:** Opens the specified project in VS Code.

**Default projects (hardcoded):**
| Alias | Path |
|-------|------|
| hex link | `C:\\Projects\\hex-link` |
| runway objects | `C:\\Projects\\runway-objects` |
| udestini | `C:\\Projects\\udestini` |

**How to add your own:** Edit the `PROJECTS` dictionary in `kosmosic_orbiton.py` or wait for the config file system (Genesis-class).

---

#### `run <script>`
**Example:** `"run myscript.py"`

**What it does:** Runs the specified Python script using `python <script>`.

**Path resolution:** Same as `open` — checks current dir, then home dir.

---

#### `file search <name>`
**Example:** `"file search report"`

**What it does:** Searches for files in the current directory matching the partial name.

---

#### `latest file [extension]`
**Examples:**
- `"latest file"` — finds the most recently modified file in current directory
- `"latest file pdf"` — finds the most recent PDF

**What it does:** Finds the most recently modified file (optionally filtered by extension) and opens it.

---

### 💪 Motivation & Control Commands

#### `motivate me`
**Example:** `"motivate me"`

**What it does:** Randomly selects one of 15 toxic roasts and speaks it to you.

**The Full Roast Database:**
1. *"The Doha apartment is not paying for itself. Get back to work, peasant."*
2. *"Your GitHub contribution graph looks like a deforestation map. Embarrassing."*
3. *"That idea you had 3 hours ago? Someone in Bangalore already shipped it."*
4. *"Your sleep schedule is a war crime. Fix yourself."*
5. *"You opened this assistant to avoid work. I see you. I judge you."*
6. *"Your code has more bugs than a Mumbai street food stall. Write a test."*
7. *"That quick break was 47 minutes ago. You disgust me."*
8. *"Your ancestors built empires. You can not even close 3 Chrome tabs."*
9. *"I ran a diagnostic on your life. Critical failure across all sectors."*
10. *"You have the focus of a goldfish on TikTok. Pathetic."*
11. *"Your last commit message was fix stuff. You are a disappointment."*
12. *"While you were procrastinating, your competitor learned Rust. You are done."*
13. *"Your to-do list is older than some civilizations. Start item one."*
14. *"I calculated your productivity. The result made my circuits cry."*
15. *"You call this grinding? I have seen sloths with more hustle."*

**Note:** There is no "gentle mode." If you cannot handle this, Orbiton is not for you.

---

#### `status report`
**Example:** `"status report"`

**What it does:** Displays session statistics: how many commands you have given, how many errors occurred, how long the session has been running.

---

#### `exam mode`
**Example:** `"exam mode"`

**What it does:** Launches study tools. Typically opens:
- A calculator
- Desmos (graphing calculator)
- A notepad/text editor

**Purpose:** Blocks distractions and sets up a focused workspace for studying.

**NLP support:** Also recognizes `"exambored"`, `"exambord"`, `"exum mode"`, `"eggsam mode"`. The NLP engine corrects these to "exam mode".

---

#### `kosmosic`
**Example:** `"kosmosic"`

**What it does:** Opens the Kosmosic study dashboard at `https://kosmosic.vercel.app/app`.

**NLP support:** Also recognizes `"kosmic"`, `"cosmic"`, `"cosmosic"`, `"kozmosic"`.

---

#### `who am i`
**Example:** `"who am i"`

**What it does:** Recalls stored user information from `~/.neuro_link_memory.json`.

**How memory works:** Orbiton can learn facts about you over time (e.g., your name, your favorite editor). This command retrieves them.

---

### 🔄 System Control Commands

#### `reboot`
**Example:** `"reboot"`

**What it does:** Restarts Orbiton cleanly. Closes the current process and spawns a new one.

**Implementation:** Uses `subprocess.Popen` to relaunch itself, then exits.

---

#### `sleep`
**Examples:**
- `"sleep"`
- `"go to sleep"`
- `"shut down"`

**What it does:** Puts Orbiton into sleep mode. It stops listening for commands until explicitly woken.

---

#### `wake` / `wake up` / `TOKYO`
**Examples:**
- `"wake"`
- `"wake up"`
- `"start"`
- `"online"`
- `"Tokyo"`

**What it does:** Wakes Orbiton from sleep mode.

**Note:** In v0.4.0+, automatic sleep was removed. Orbiton stays awake indefinitely until you explicitly tell it to sleep. This prevents accidental sleep during long work sessions.

---

#### `help`
**Example:** `"help"`

**What it does:** Displays the full command table in the terminal.

**Known bug:** Sometimes "help" does not execute the help handler. If this happens, type `help` instead of saying it, or try saying it twice.

**NLP support:** Also recognizes `"hell"`, `"hellp"`, `"halp"`, `"helf"`, `"elpe"`.

---

## 7. Typing Commands (No Microphone)

If your microphone is broken, missing, or you are in a library, you can type commands directly into the terminal.

### How to Type
1. Run `python kosmosic_orbiton.py`
2. When you see the prompt, type your command and press **Enter**.
3. Orbiton processes it exactly as if you had spoken it.

### Typed vs Spoken: The Only Difference
- **Typed commands** skip the speech recognition step.
- **Typed commands** do not need the wake word. You can type `search python` immediately without saying "Tokyo" first.
- **Voice commands** require "Tokyo" to wake the listener.

### Pro Tip: Mixed Mode
Many power users type complex commands (like `open project hex link`) but use voice for quick commands (like `motivate me` or `what time is it`). Use whatever is faster for the moment.

---

## 8. The Neuro-Link Intelligence System

Orbiton's brain is `neuro_link_intel.py`. It is not magic. It is a collection of Python classes that clean up your messy speech and figure out what you actually want.

### The Three Brains

#### 1. NaturalLanguageProcessor (NLP)
**Job:** Turn sloppy human speech into clean, structured commands.

**What it does:**

**A. Contraction Expansion**
| You Say | Orbiton Hears |
|---------|---------------|
| "what's" | "what is" |
| "i'm" | "i am" |
| "don't" | "do not" |
| "can't" | "cannot" |
| "gonna" | "going to" |
| "wanna" | "want to" |
| "lemme" | "let me" |
| "dunno" | "do not know" |

**B. Filler Word Stripping**
Removes: `um`, `uh`, `like`, `you know`, `i mean`, `basically`, `literally`, `actually`, `honestly`, `seriously`, `so`, `well`, `okay`, `ok`

Example: `"um like search for uh python basically"` -> `"search for python"`

**C. Homophone Correction**
Speech recognition is imperfect. Orbiton maps common misheard phrases to intended commands.

| Misheard | Corrected To |
|----------|--------------|
| exambored | exam mode |
| exambord | exam mode |
| exum mode | exam mode |
| eggsam mode | exam mode |
| hell / hellp / halp / helf / elpe | help |
| kosmic / cosmic / cosmosic / kozmosic | kosmosic |
| stutus / statas / stattus | status |
| meter / meeter / meytar | metar |
| flight radar / flightrader | flightradar |
| street view / streetvue / strretview | streetview |
| clipbored / clipbord | clipboard |
| motivait / motivete / motovate | motivate |
| rekognize / reeboot / rebbot / rebote | reboot |
| whoami / huami / hooami | who am i |

**D. Intent Extraction**
The NLP engine recognizes question patterns and routes them:

| Pattern | Action |
|---------|--------|
| "what is the weather in X" | Extracts X as city, triggers weather |
| "what is the time" | Triggers time command |
| "tell me about X" | Triggers knowledge lookup for X |
| "who is X" | Triggers knowledge lookup for X |
| "where is X" | Triggers knowledge lookup for X |
| "how do you X" | Triggers knowledge lookup for X |

---

#### 2. MathNormalizer
**Job:** Convert spoken math into safe Python expressions.

**The Pipeline:**
1. Strip the word `calculate` from the beginning.
2. Replace multi-word operators first (order matters — longest first):
   - `"to the power of"` -> `**`
   - `"divided by"` -> `/`
   - `"multiplied by"` -> `*`
3. Replace single-word operators:
   - `"times"`, `"into"`, `"x"` -> `*`
   - `"over"` -> `/`
   - `"minus"`, `"subtract"` -> `-`
   - `"plus"`, `"add"` -> `+`
   - `"mod"`, `"modulo"` -> `%`
   - `"squared"` -> `**2`
   - `"cubed"` -> `**3`
4. Convert word numbers to digits:
   - `"twenty five"` -> `25`
   - `"three hundred"` -> `300`
   - `"two million"` -> `2000000`
5. Collapse multiple operators and clean up spaces.

**Example Walkthrough:**
```
Input:  "calculate twenty five divided by five plus two squared"
Step 1: "twenty five divided by five plus two squared"
Step 2: "twenty five / five + two **2"
Step 3: "25 / 5 + 2 **2"
Step 4: eval("25 / 5 + 2 **2") = 9.0
Output: "9.0"
```

---

#### 3. KnowledgeEngine + WikimediaScraper
**Job:** Answer questions by looking things up.

**Local Knowledge:**
Orbiton has built-in mini-databases for:
- **Moon Phases** — New Moon, Waxing Crescent, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Waning Crescent.
- **Aviation Facts** — V1, V2, Mach, ICAO, Squawk, METAR, TAF, etc.
- **Space Facts** — ISS orbit altitude, Mars distance, black hole definitions, light year definition, Big Bang summary.

*(Note: Constellations were removed in v0.5.0 to reduce bundle size. They now route to Wikipedia.)*

**Wikipedia Lookup:**
If local knowledge does not have the answer, Orbiton:
1. Queries `https://en.wikipedia.org/api/rest_v1/page/summary/<topic>`
2. Saves the result to `~/.neuro_link_wiki_cache/<topic>.txt`
3. Returns the first 500 characters
4. Speaks the summary

**Custom Intel:**
You can add your own knowledge bases by creating JSON files in `~/.neuro_link_intel/`:
```bash
mkdir -p ~/.neuro_link_intel
```

```json
// ~/.neuro_link_intel/intel_chemistry.json
{
  "water": "H2O is the chemical formula for water.",
  "oxygen": "Oxygen is a chemical element with symbol O and atomic number 8."
}
```
Orbiton will automatically load these on startup.

---

## 9. Configuration: Making Orbiton Yours

All configuration lives in the `CONFIG` dictionary at the top of `kosmosic_orbiton.py`. In the future (Genesis-class), this will move to an external JSON/YAML file.

### The CONFIG Dictionary

```python
CONFIG = {
    "chrome_path": {
        "Windows": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Linux": "/usr/bin/google-chrome"
    },
    "user_home": str(Path.home()),
    "audio_timeout": 8,
    "phrase_limit": 6,
    "max_errors_before_reset": 50,
    "wake_word": "tokyo",
    "memory_file": str(Path.home() / ".neuro_link_memory.json"),
    "voice": "en-US-AriaNeural",
}
```

### What Each Key Means

| Key | Default | What It Controls |
|-----|---------|------------------|
| `chrome_path` | OS-specific | Where Chrome lives on your system. Orbiton uses this to open URLs. If Chrome is not found, it falls back to the system default browser. |
| `user_home` | `~` | Your home directory. Used for path resolution. |
| `audio_timeout` | `8` | How many seconds Orbiton listens after the wake word before giving up. |
| `phrase_limit` | `6` | Maximum phrase duration in seconds. Prevents Orbiton from listening forever if you start rambling. |
| `max_errors_before_reset` | `50` | If 50 consecutive errors occur (e.g., microphone disconnects), Orbiton automatically resets the audio listener to recover. |
| `wake_word` | `"tokyo"` | The word that wakes Orbiton. Must be lowercase. |
| `memory_file` | `~/.neuro_link_memory.json` | Where your personal facts are stored. |
| `voice` | `"en-US-AriaNeural"` | The Edge TTS voice profile. Change this to any Edge TTS voice (e.g., `"en-US-JennyNeural"`, `"en-GB-SoniaNeural"`). |

### How to Change the Wake Word
1. Open `kosmosic_orbiton.py` in a text editor.
2. Find the `CONFIG` dictionary.
3. Change `"wake_word": "tokyo"` to `"wake_word": "computer"` (or whatever you want).
4. Save the file.
5. Restart Orbiton.

**Important:** The wake word must be a single word. Multi-word wake words (like "hey orbiton") are not supported in Tokyo-class.

### How to Change the Voice
1. Open `kosmosic_orbiton.py`.
2. Find `"voice": "en-US-AriaNeural"`.
3. Replace with any valid Edge TTS voice. Popular options:
   - `en-US-AriaNeural` (default, friendly)
   - `en-US-JennyNeural` (professional)
   - `en-GB-SoniaNeural` (British)
   - `en-AU-NatashaNeural` (Australian)
   - `en-IN-NeerjaNeural` (Indian English)
4. Save and restart.

**Full list of Edge TTS voices:** Visit `https://speech.microsoft.com/portal/voicegallery` or run `edge-tts --list-voices` in your terminal.

### How to Add Project Shortcuts
1. Open `kosmosic_orbiton.py`.
2. Find the `PROJECTS` dictionary:
```python
PROJECTS = {
    "hex link": r"C:\\Projects\\hex-link",
    "runway objects": r"C:\\Projects\\runway-objects",
    "udestini": r"C:\\Projects\\udestini",
}
```
3. Add your own:
```python
PROJECTS = {
    "hex link": r"C:\\Projects\\hex-link",
    "runway objects": r"C:\\Projects\\runway-objects",
    "udestini": r"C:\\Projects\\udestini",
    "my app": r"C:\\Users\\You\\Projects\\my-app",
}
```
4. Save and restart.
5. Now you can say: `"open project my app"`

---

## 10. Files, Folders, and Projects

### Path Resolution Logic
When you say `"open downloads"`, Orbiton resolves the path in this order:

1. **Known aliases** — `downloads`, `documents`, `desktop`, `pictures`, `videos`, `music` map to your OS standard folders.
2. **Relative path** — Checks if `downloads` exists in the current working directory.
3. **Home directory** — Checks if `downloads` exists in `~` (your home folder).
4. **Absolute path** — If you gave a full path like `C:\\Users\\You\\Downloads`, it uses that directly.

### The `go to` Command
This changes Orbiton's internal working directory. It affects:
- Where `open` looks for files
- Where `run` looks for scripts
- Where `file search` searches
- Where `latest file` scans

**Special navigation keywords:**
| Keyword | Action |
|---------|--------|
| `parent` | Go up one directory (`cd ..`) |
| `back` | Go to previous directory |
| `up` | Same as `parent` |

### VS Code Project Launching
When you say `"open project <name>"`, Orbiton:
1. Looks up `<name>` in the `PROJECTS` dictionary.
2. Runs `code <path>` (the VS Code CLI command).
3. VS Code opens that folder as a workspace.

**Prerequisite:** You must have the `code` command in your system PATH. If `code` is not recognized:
- **Windows:** VS Code usually adds this automatically during install.
- **macOS:** Open VS Code, press `Cmd+Shift+P`, type "Shell Command: Install 'code' command in PATH".
- **Linux:** Same as macOS, or symlink manually.

---

## 11. The Memory System

Orbiton can remember facts about you. This is not AI memory. It is a simple JSON file that stores key-value pairs.

### The Memory File
Location: `~/.neuro_link_memory.json`

Example contents:
```json
{
  "name": "Ayman",
  "favorite_language": "Python",
  "location": "Doha",
  "last_project": "hex-link"
}
```

### How Memory Is Updated
Currently, memory is updated through code paths (e.g., if you tell Orbiton your name during a specific interaction). In future versions (Odyssey-class), this will be more conversational.

### How to Edit Memory Manually
1. Open `~/.neuro_link_memory.json` in any text editor.
2. Add, edit, or delete key-value pairs.
3. Save the file.
4. Orbiton reads this file on startup and when `who am i` is called.

**Example:** Add your birthday so Orbiton can wish you happy birthday:
```json
{
  "name": "Alex",
  "birthday": "1995-03-15"
}
```

### The `who am i` Command
This command reads the memory file and speaks back what it knows about you. If the file is empty or missing, it will say it does not know you yet.

---

## 12. Knowledge & Wikipedia Lookup

### Built-In Knowledge Bases
Orbiton ships with three built-in knowledge categories:

1. **Moon Phases** — New Moon, Waxing Crescent, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Waning Crescent.
2. **Aviation Facts** — V1, V2, Mach, ICAO, Squawk, METAR, TAF, etc.
3. **Space Facts** — ISS orbit altitude, Mars distance, black hole definitions, light year definition, Big Bang summary.

### Wikipedia Integration
For topics not in the built-in database, Orbiton queries Wikipedia's REST API:
- **Endpoint:** `https://en.wikipedia.org/api/rest_v1/page/summary/<topic>`
- **Timeout:** 5 seconds
- **Cache:** Results are saved to `~/.neuro_link_wiki_cache/<topic>.txt`
- **Return limit:** First 500 characters

### Adding Custom Intel
Create a JSON file in `~/.neuro_link_intel/` with the naming pattern `intel_<name>.json`:

```bash
mkdir -p ~/.neuro_link_intel
```

```json
// ~/.neuro_link_intel/intel_chemistry.json
{
  "water": "H2O is the chemical formula for water.",
  "oxygen": "Oxygen is a chemical element with symbol O and atomic number 8."
}
```
Restart Orbiton. Now you can say `"tell me about oxygen"` and it will use your custom intel.

---

## 13. Platform-Specific Deep Dive

### Windows
**Full support.**
- **File Explorer:** `open` commands launch Windows Explorer.
- **VS Code projects:** Hardcoded paths in `PROJECTS` use `C:\\Projects\\...`. Edit these to match your setup.
- **TTS:** If Edge TTS is offline, falls back to PowerShell TTS (`Add-Type -AssemblyName System.Speech`).
- **Headphone detection:** Uses Windows Management Instrumentation (WMI) to detect Bluetooth audio devices.

**Windows-specific setup:**
- If Chrome is not installed at the default path, edit `CONFIG["chrome_path"]["Windows"]`.
- If you use VS Code but `code` is not in PATH, add it: Open VS Code -> `Ctrl+Shift+P` -> "Shell Command: Install 'code' command in PATH".

### macOS
**Full support.**
- **File opening:** Uses the `open` command.
- **TTS:** Uses `say` command as fallback if Edge TTS is offline.
- **Audio:** Uses `afplay` for sound effects.
- **Headphone detection:** Uses `system_profiler` to find Bluetooth audio devices.

**macOS-specific setup:**
- If Chrome is not at `/Applications/Google Chrome.app`, edit `CONFIG["chrome_path"]["Darwin"]`.
- You may need to grant Terminal microphone permissions in **System Preferences -> Security & Privacy -> Privacy -> Microphone**.

### Linux
**Partial support.**
- **File opening:** Uses `xdg-open`.
- **TTS:** Uses `spd-say` (Speech Dispatcher) as fallback.
- **Headphone detection:** Best-effort. May not detect all Bluetooth headsets.
- **Clipboard:** Requires `xclip` or `xsel` installed for `clipboard` command.

**Linux-specific setup:**
```bash
# Install clipboard dependencies
sudo apt-get install xclip xsel

# Install speech dispatcher (for TTS fallback)
sudo apt-get install speech-dispatcher

# If Chrome is not at /usr/bin/google-chrome, find it:
which google-chrome
# Then edit CONFIG["chrome_path"]["Linux"]
```

**Known Linux issues:**
- Edge TTS offline fallback is silent (no error message, just no sound).
- Headphone auto-detect is unreliable on some distributions.

---

## 14. Hacking Orbiton: Adding Commands

This section is for developers who want to extend Orbiton.

### The Anatomy of a Command
Every command has three parts:
1. **Intent Pattern** — A regex that recognizes the command
2. **Handler Method** — A Python method that executes the command
3. **NLP Support** (optional) — Homophone corrections for voice reliability

### Step-by-Step: Adding a "Translate" Command

#### Step 1: Add the Handler
Open `kosmosic_orbiton.py` and add a method to the `CommandEngine` class:

```python
def handle_translate(self, query: str):
    # Translate text using Google Translate.
    url = f"https://translate.google.com/?sl=auto&tl=en&text={quote(query)}"
    self.open_chrome(url)
    msg = f"Translating: {query}"
    self.ui.show_success(msg)
    self.speak(msg)
```

#### Step 2: Add the Intent Pattern
Find the `IntentParser.PATTERNS` list and add:

```python
(r"^(?:translate|translation|what does)\s+(.+)", "translate"),
```

#### Step 3: Add NLP Support (Optional)
Open `neuro_link_intel.py` and add to `NaturalLanguageProcessor.HOMOPHONES`:

```python
"translait": "translate",
"translete": "translate",
"translat": "translate",
```

#### Step 4: Add to Help Table
Find `ALL_COMMANDS` in `kosmosic_orbiton.py` and add:

```python
("🌍 Translate", "translate <text>", "Google Translate anything"),
```

#### Step 5: Add Tests
Create `tests/url_engine/test_translate_urls.py`:

```python
import pytest

def test_translate_url(engine):
    opened = []
    engine.open_chrome = lambda url, *args: opened.append(url)
    engine.handle_translate("hello world")
    assert len(opened) == 1
    assert "translate.google.com" in opened[0]
    assert "hello" in opened[0]
```

Create `tests/core_logic/test_intent_parser.py` addition:

```python
def test_translate_intent(parser):
    intent, arg = parser.parse("translate hello to french")
    assert intent == "translate"
    assert arg == "hello to french"
```

Run tests:
```bash
pytest tests/url_engine/test_translate_urls.py -v
pytest tests/core_logic/test_intent_parser.py -v
```

### Code Style Rules
- **4 spaces** for indentation. No tabs.
- **Type hints** encouraged but not required.
- **Docstrings** for public methods. One line is fine.
- **Naming:** `handle_*` for command methods, `test_*` for tests.
- **No trailing whitespace.**

### What Gets Rejected
- Code that breaks existing commands.
- Features requiring heavy GUI frameworks (no Tkinter, no PyQt).
- Features that phone home or track users.
- AI-generated code without disclosure.
- References to *Project Hail Mary*.

---

## 15. Testing & Quality Assurance

Orbiton has a full pytest suite with 151+ tests across 7 CI workflows.

### Running Tests Locally

```bash
# Run everything
pytest tests/ -v

# Run by category
pytest tests/core_logic/ -v
pytest tests/url_engine/ -v
pytest tests/compute/ -v
pytest tests/launch/ -v
pytest tests/system/ -v
pytest tests/integration/ -v

# Run a single test
pytest tests/compute/test_security.py::test_malicious_input_rejected -v

# With coverage
pytest tests/ -v --cov=kosmosic_orbiton --cov-report=xml
```

### Test Categories

| Category | Files | Tests | What It Covers |
|----------|-------|-------|----------------|
| **Core Logic** | 4 | ~30 | Intent parsing, command patterns, NLP normalization, unknown commands |
| **URL Engine** | 8 | ~16 | URL generation for search, YouTube, maps, weather, airport, METAR, flight tracking, Street View |
| **Compute** | 7 | ~20 | Math expressions, security (injection prevention), constants, square roots |
| **Launch** | 8 | ~29 | File opening, folder navigation, VS Code projects, Python scripts, clipboard, exam mode |
| **System** | 5 | ~15 | Session stats, time, motivation engine, headphone detection, status reports |
| **Integration** | 6 | ~12 | End-to-end flows: search, maps, weather, YouTube, file open, project launch |
| **Pylint** | — | — | Code quality and style checks |

### CI Workflows
Every category has its own GitHub Actions workflow:
- `core-logic.yml`
- `url-engine.yml`
- `compute.yml`
- `launch.yml` (runs on **Windows** — because file operations are OS-specific)
- `system.yml`
- `integration.yml`
- `pylint.yml`

### Test Fixtures (conftest.py)
The test suite provides these fixtures:

| Fixture | Purpose |
|---------|---------|
| `mock_ui` | Mocked `NeuroInterface` with counters |
| `mock_voice` | Mocked `VoiceManager` |
| `mock_memory` | Mocked `UserMemory` |
| `mock_intel` | Mocked `IntelligenceOrchestrator` |
| `engine` | `CommandEngine` built from mocks |
| `parser` | Fresh `IntentParser()` instance |

### Known Flaky Tests
| Test | Issue | Workaround |
|------|-------|----------|
| `test_navigate_parent` | Platform-specific subprocess mocking | Patched for Windows/Linux |
| `test_open_downloads` | `Path.exists()` behavior on CI | Mocked `Path.exists` and `is_dir` |

---

## 16. Troubleshooting Bible

### Installation Issues

#### `ModuleNotFoundError: No module named 'speech_recognition'`
**Fix:**
```bash
pip install speechrecognition
```
*(Note: the package name is `speechrecognition` without the underscore, but you import it as `speech_recognition`.)*

#### `ModuleNotFoundError: No module named 'rich'`
**Fix:**
```bash
pip install rich
```

#### `ModuleNotFoundError: No module named 'edge_tts'`
**Fix:**
```bash
pip install edge-tts
```

#### `ImportError: cannot import name 'get_intelligence' from 'neuro_link_intel'`
**Fix:** Make sure you are running Orbiton from the `Kosmosic-Orbiton` directory. The import is relative to the current directory.
```bash
cd Kosmosic-Orbiton
python kosmosic_orbiton.py
```

### Voice / Microphone Issues

#### Orbiton does not hear me at all
**Checklist:**
1. Is your microphone plugged in and working? Test it with your OS sound settings.
2. Does your terminal have microphone permissions?
   - **macOS:** System Preferences -> Security & Privacy -> Microphone -> Check your terminal app.
   - **Windows:** Settings -> Privacy -> Microphone -> Allow apps access.
3. Is your microphone muted?
4. Is another app (Zoom, Discord) hogging the microphone? Close other apps.
5. Try typing commands instead to verify Orbiton works at all.

#### Orbiton hears me but does nothing
**Checklist:**
1. Are you saying the wake word first? Say `"Tokyo"`, pause, then say your command.
2. Is Orbiton asleep? Say `"wake"` or `"TokYO"`.
3. Check your terminal output. Is there an error message?
4. Try typing the exact same command. If typing works but voice does not, the speech recognition is failing.

#### Speech recognition is very inaccurate
**Fixes:**
- Speak more clearly.
- Reduce background noise.
- Use a headset instead of a built-in mic.
- Move closer to the microphone.
- Check if your speech recognition engine (Google Web Speech API) requires internet. If you are offline, voice recognition may not work.

#### The "self-listening" bug
**Symptom:** Orbiton speaks, then immediately hears its own voice and triggers a random command (usually an intel lookup).
**Why:** Your speakers are loud enough for the microphone to pick up the TTS output.
**Fixes:**
- **Use headphones/headset.** This is the intended design.
- Lower your speaker volume.
- Move the microphone farther from the speakers.
- This is a known bug and will be fixed in a future update.

### Command Issues

#### `"help"` does not work
**Symptom:** Saying `"help"` does nothing.
**Workarounds:**
- Type `help` instead of saying it.
- Say it twice.
- Try the misheard variants: `"hell"`, `"halp"`, `"helf"`.
**Status:** Known bug. Will be fixed.

#### `"exam board"` triggers a search instead of exam mode
**Symptom:** Saying `"exam board"` (two words) opens Google instead of launching study tools.
**Why:** The NLP catches `"exambored"` (one word) but the two-word variant falls through.
**Workaround:** Say `"exam mode"` clearly, or `"exambored"`.
**Status:** Known bug.

#### `calculate` gives wrong answers for spoken math
**Symptom:** `"calculate two times two"` returns an error.
**Fix:** This was fixed in v0.6.2. Update to the latest version.
```bash
git pull origin main
```

### TTS / Voice Output Issues

#### Orbiton does not speak
**Checklist:**
1. Is `edge-tts` installed? `pip install edge-tts`
2. Do you have internet? Edge TTS requires internet to download voice data.
3. Are your speakers/headphones working?
4. Check if the system TTS fallback is working:
   - **Windows:** PowerShell should be able to run `Add-Type -AssemblyName System.Speech`.
   - **macOS:** `say` command should work in terminal.
   - **Linux:** `spd-say` should be installed.

#### Edge TTS is installed but silent when offline
**Symptom:** `edge-tts` is installed, you have no internet, and Orbiton makes no sound.
**Why:** The fallback to system TTS is silent if `edge-tts` is installed but unreachable.
**Workaround:** Uninstall `edge-tts` to force system TTS fallback:
```bash
pip uninstall edge-tts
```
**Status:** Known bug on Linux especially.

### File / Project Issues

#### `"open project X"` says project not found
**Fix:** Edit the `PROJECTS` dictionary in `kosmosic_orbiton.py` to point to your actual project paths. The default paths are `C:\\Projects\\...` which probably do not exist on your machine.

#### `code` command not found
**Fix:** Add VS Code to your system PATH. See [Platform-Specific Deep Dive](#13-platform-specific-deep-dive).

#### Files open in the wrong app
**Fix:** Orbiton uses your OS default application. Change the default app in your OS settings, or use the full path to the app you want.

### Performance Issues

#### Orbiton is slow to respond
**Possible causes:**
- Slow internet (for Edge TTS or Wikipedia lookups)
- Heavy CPU load from other apps
- Microphone latency

**Fixes:**
- Use typed commands instead of voice for faster response.
- Close unnecessary browser tabs and apps.
- Check if `max_errors_before_reset` is being hit (indicates audio issues).

### Error Recovery

#### Orbiton crashes with 50 consecutive errors
**Symptom:** After 50 audio/microphone errors, Orbiton resets the listener.
**Why:** This is a safety feature to recover from bad microphone states.
**Fix:** Check your microphone connection and permissions.

---

## 17. Architecture Reference

### File Structure
```
Kosmosic-Orbiton/
├── kosmosic_orbiton.py          # Main entry point. CommandEngine, UI, voice loop.
├── neuro_link_intel.py          # Intelligence module. NLP, math, knowledge.
├── requirements.txt             # Python dependencies.
├── CHANGELOG.md                 # Version history.
├── PHILOSOPHY.md                # Why Orbiton exists.
├── ROADMAP.md                   # Future generations.
├── CONTRIBUTING.md              # How to contribute.
├── CONTRIBUTORS.md              # Who built this.
├── TEST_STATUS.md               # Per-test CI status.
├── TESTS.md                     # Test architecture docs.
├── WORKFLOWS.md                 # CI/CD configuration.
├── tests/                       # Full pytest suite.
│   ├── conftest.py              # Shared fixtures.
│   ├── core_logic/              # Intent & pattern tests.
│   ├── url_engine/              # URL generation tests.
│   ├── compute/                 # Math & security tests.
│   ├── launch/                  # File & project tests.
│   ├── system/                  # Status & time tests.
│   └── integration/             # End-to-end flow tests.
└── .github/workflows/           # CI/CD definitions.
    ├── core-logic.yml
    ├── url-engine.yml
    ├── compute.yml
    ├── launch.yml
    ├── system.yml
    ├── integration.yml
    ├── pylint.yml
    ├── filediff.yml
    └── python-tests.yml
```

### Class Breakdown

#### `kosmosic_orbiton.py`

| Class | Responsibility |
|-------|---------------|
| `CommandEngine` | The heart. Routes commands, manages state, handles execution. |
| `IntentParser` | Regex-based command recognition. Maps text to intent + argument. |
| `NeuroInterface` | Terminal UI using `rich`. Shows success/error/status panels. |
| `VoiceManager` | Text-to-speech. Handles Edge TTS and system fallbacks. |
| `UserMemory` | Reads/writes `~/.neuro_link_memory.json`. |
| `AudioListener` | Speech recognition loop. Wake word detection, audio timeout. |

#### `neuro_link_intel.py`

| Class | Responsibility |
|-------|---------------|
| `NaturalLanguageProcessor` | Cleans speech: contractions, fillers, homophones. |
| `MathNormalizer` | Converts spoken math to safe Python expressions. |
| `KnowledgeEngine` | Local knowledge base lookup. |
| `WikimediaScraper` | Wikipedia REST API queries with local caching. |
| `IntelligenceOrchestrator` | Combines all intelligence modules. Decides: command? knowledge? search? |

### Data Flow (Voice Command)

```
You speak -> Microphone -> AudioListener
                                    |
                         SpeechRecognition (Google Web API)
                                    |
                         Raw text: "tokyo search python"
                                    |
                         NaturalLanguageProcessor.normalize()
                                    |
                         Clean text: "search python"
                                    |
                         IntentParser.parse()
                                    |
                         Intent: "search", Arg: "python"
                                    |
                         CommandEngine.handle_search("python")
                                    |
                         open_chrome("https://google.com/search?q=python")
                                    |
                         NeuroInterface.show_success("Searching: python")
                                    |
                         VoiceManager.speak("Searching python")
                                    |
                         You hear the result
```

### Data Flow (Knowledge Query)

```
You speak -> "tell me about black holes"
                                    |
                         NLP normalize -> "tell me about black holes"
                                    |
                         IntelligenceOrchestrator.process()
                                    |
                         Is it a time query? No.
                         Is it a weather query? No.
                         Is it a general knowledge question? Yes.
                                    |
                         KnowledgeEngine.lookup("black holes")
                                    |
                         Found in local Space Facts? Yes -> Return fact.
                         Not found? -> WikimediaScraper.search_topic("black holes")
                                    |
                         Cache result to ~/.neuro_link_wiki_cache/black_holes.txt
                                    |
                         Return first 500 chars
                                    |
                         VoiceManager.speak("A black hole is a region of spacetime...")
```

---

## 18. The Roadmap: Where Orbiton Is Going

Orbiton evolves through **generations**, each named after a model class.

### Generation 1 — Tokyo (Current, v0.6.2)
**Status:** Active development.  
**What works:** Voice commands, web search, file management, aviation tools, toxic motivation, local knowledge, Wikipedia scraping, cross-platform support.  
**Known bugs:** Self-listening, help command unresponsive, exam board NLP, Linux headphone detection, Edge TTS offline fallback, hardcoded Windows paths.

### Generation 2 — Odyssey (Planned, v2.x.x)
**Theme:** Large-scale growth. Advanced reasoning and memory.
**Features:**
- Local LLM integration (Ollama, llama.cpp)
- Cloud LLM fallback for complex queries
- Long-term memory that persists across sessions and builds a user model
- Personalization engine (adapts commands, roasts, suggestions)
- Scraper living on your PC (gathers info, converts to JSON)
- OTA intel updates (download new knowledge bases without updating the whole app)
- More headset support (Sony, Bose, AirPods)
- Wake word customization
- Multiple voices
- Multi-language support

### Generation 3 — Genesis (Planned, v3.x.x)
**Theme:** Agentic behavior. True automation.
**Features:**
- Long-running tasks ("remind me in 2 hours")
- Predictive execution (suggest commands based on time/habits)
- Multi-step workflows ("study mode" opens Kosmosic, sets timer, enables DND)
- Talk to others (share commands/intel between Orbiton instances)
- System info (CPU/RAM monitoring)
- Kill processes ("kill Chrome")
- Restart services

### Generation 4 — Micron (Planned, v4.x.x — ROI-dependent)
**Theme:** Lite version for constrained environments.
**Features:**
- Remove `rich` dependency (plain text only)
- Remove `edge-tts` dependency (system TTS only)
- Strip built-in intel databases (load on demand)
- Target: Raspberry Pi, old laptops, minimal VMs

### Generation 5 — Aphrodite (Planned, v5.x.x)
**Theme:** Expansion beyond the original vision.
**Features:**
- Send emails via voice
- Place calls using system dialer/VoIP
- Calendar management
- IoT & smart home (lights, thermostat, smart plugs)
- Full wake word customization
- Full language packs

### Generation 6 — Singularity (Vision, v6.x.x)
**Theme:** Full autonomy. The second user of your computer.
**Features:**
- Wearables (smartwatch companion, earbud firmware)
- Smart glasses (HUD overlay)
- Single-board computers (dedicated Orbiton appliance)
- Replaces bloatware AIs (Cortana, Siri)
- Predictive everything
- Self-maintenance
- Multi-device continuity

### Generation 7 — Utopia (Final Vision, v7.x.x)
**Theme:** The absolute top.
**Features:**
- Global-scale platform evolution
- Interconnected ecosystem (all devices talk)
- True ambient intelligence
- The second user of your computer — it knows your workflow better than you do

### Pre-2.0 Checklist (Odyssey Release)
Before Generation 2 is declared:
- [ ] Local LLM integration working offline
- [ ] Long-term memory persists across sessions
- [ ] Personalization engine adapts to user habits
- [ ] Test suite passes 100% on all three OSes
- [ ] Config system replaces hardcoded values
- [ ] Auth system for multi-user support
- [ ] Website for downloads, docs, and intel sharing
- [ ] Self-listening bug resolved
- [ ] Help command bug resolved
- [ ] Documentation complete

---

## 19. Contributing to Orbiton

### Who Can Contribute
Anyone. Grade 10 student? Welcome. Senior dev with opinions? Also welcome. Just make it work and make it fit.

### How to Contribute (Non-Owner)
1. **Fork the repo** or ask for collaborator access.
2. **Create a branch:** `git checkout -b your-feature-name`
3. **Make your changes.**
4. **Test everything.** Run `pytest tests/ -v`. All tests must pass.
5. **Open a Pull Request.** No issue required, but you can open one to discuss first.
6. **Wait for review.** If it works and aligns with the philosophy, it gets merged.

### Quality Checklist Before PR
- [ ] It works on your machine. Test the actual command.
- [ ] You documented errors you hit and how you fixed them.
- [ ] You did not create new bugs in existing commands.
- [ ] You added tests if you added something new.
- [ ] Your change aligns with the philosophy (voice-first, terminal-based, no bloat).
- [ ] You tested on your OS. If only Windows, say so in the PR.

### Testing Requirements for PRs
| What you added | Test file to create/modify |
|----------------|---------------------------|
| New URL-opening command | `tests/url_engine/test_<command>_urls.py` |
| New intent/parser pattern | `tests/core_logic/test_intent_parser.py` |
| New file/folder behavior | `tests/launch/test_<feature>.py` |
| New math/utility | `tests/compute/test_<feature>.py` |
| New system feature | `tests/system/test_<feature>.py` |
| End-to-end flow | `tests/integration/test_<feature>_flow.py` |

### Voice Command PRs
Voice commands are hard to unit test. If you add or modify one, **record a screen capture** showing:
1. You saying the wake word ("Tokyo").
2. You giving the command.
3. Orbiton responding correctly.

Upload the video to the PR description or link it (YouTube unlisted, Google Drive, etc.).

### Code Style
- 4 spaces for indentation. No tabs.
- Type hints encouraged but not required.
- Docstrings for public methods.
- Match existing naming: `handle_*` for commands, `test_*` for tests.
- No trailing whitespace.

### What Will Get Rejected
- Code that breaks existing commands.
- Heavy GUI frameworks (Tkinter, PyQt).
- Features that phone home or track users.
- AI-generated code without disclosure.
- References to *Project Hail Mary*.

---

## 20. Glossary of Terms

| Term | Definition |
|------|------------|
| **Wake Word** | The word that activates Orbiton from sleep. Default: `"tokyo"`. |
| **Tokyo-class** | The current generation of Orbiton (v0.x). Basic reasoning and voice commands. |
| **Neuro-Link** | Orbiton's intelligence module (`neuro_link_intel.py`). NLP, math, knowledge. |
| **TTS** | Text-to-Speech. The technology that makes Orbiton talk back to you. |
| **Edge TTS** | Microsoft's neural text-to-speech engine. Requires internet. |
| **NLP** | Natural Language Processing. The system that cleans up your messy speech. |
| **Intent** | What Orbiton thinks you want to do (e.g., "search", "open", "calculate"). |
| **Handler** | The Python method that executes an intent (e.g., `handle_search`). |
| **Homophone** | Words that sound alike but mean different things. Orbiton corrects misheard homophones (e.g., "exambored" -> "exam mode"). |
| **METAR** | Meteorological Aerodrome Report. A standardized aviation weather report. |
| **ICAO** | International Civil Aviation Organization. The four-letter airport codes (e.g., `KJFK`, `EGLL`). |
| **Toxic Motivation** | Orbiton's roast engine. Harsh accountability statements designed to make you work. |
| **Self-Listening Bug** | When Orbiton hears its own TTS output and triggers unintended commands. |
| **CONFIG** | The configuration dictionary in `kosmosic_orbiton.py`. Controls timeouts, voice, wake word, etc. |
| **Intel** | Knowledge base files. Built-in or custom JSON files in `~/.neuro_link_intel/`. |
| **Session** | One continuous run of Orbiton from start to exit. |
| **CI/CD** | Continuous Integration / Continuous Deployment. The GitHub Actions that run tests automatically. |
| **Pytest** | The Python testing framework used by Orbiton. |
| **Fixture** | A reusable test component (e.g., a mock engine) provided by `conftest.py`. |
| **Odyssey-class** | Planned Generation 2. Local LLM, long-term memory, personalization. |
| **Genesis-class** | Planned Generation 3. Agentic behavior, predictive execution. |
| **Singularity-class** | Vision Generation 6. Full autonomy, multi-device ecosystem. |
| **Kosmosic** | The company behind Orbiton. Also the name of the study dashboard. |
| **Slopware** | A term used in the philosophy to describe bloated, low-quality software. Orbiton is the opposite. |

---

## QUICK REFERENCE CARD

### Essential Commands (Print This Out)

| Command | Example | Result |
|---------|---------|--------|
| Wake | `"Tokyo"` | Orbiton listens |
| Search | `"search python"` | Google opens |
| YouTube | `"youtube lofi"` | YouTube opens |
| Math | `"calculate 25 * 4"` | Speaks "100" |
| Weather | `"weather doha"` | Weather search |
| Files | `"open downloads"` | Opens Downloads folder |
| Project | `"open project hex link"` | VS Code opens project |
| Maps | `"maps eiffel tower"` | Google Maps opens |
| Time | `"what time is it"` | Speaks current time |
| Roast | `"motivate me"` | Speaks a toxic roast |
| Sleep | `"sleep"` | Orbiton stops listening |
| Wake | `"wake"` or `"Tokyo"` | Orbiton resumes |
| Reboot | `"reboot"` | Restarts Orbiton |
| Help | `"help"` | Shows all commands |

### File Locations (Know Where Your Data Lives)

| File | Path | What It Stores |
|------|------|----------------|
| User Memory | `~/.neuro_link_memory.json` | Facts about you |
| Wiki Cache | `~/.neuro_link_wiki_cache/` | Wikipedia lookups |
| Custom Intel | `~/.neuro_link_intel/` | Your knowledge bases |
| Source Code | `Kosmosic-Orbiton/kosmosic_orbiton.py` | Main application |
| Intelligence | `Kosmosic-Orbiton/neuro_link_intel.py` | NLP & knowledge |

### Keyboard Shortcuts (Terminal)

| Key | Action |
|-----|--------|
| `Ctrl+C` | Force quit Orbiton |
| `Ctrl+Z` | Suspend Orbiton (resume with `fg`) |
| `Up Arrow` | Recall previous typed command (terminal history) |
| `Tab` | Auto-complete file paths when typing |

---

> **"Your ancestors built empires. You cannot even close 3 Chrome tabs."**  
> — Orbiton, pushing you toward mastery

**© 2026 Kosmosic**  
**License:** GNU General Public License v3.0  
**Repo:** https://github.com/AymanHaidry/Kosmosic-Orbiton  
**Website:** https://theorbiton.vercel.app
