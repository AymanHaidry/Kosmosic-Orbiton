# 🔧 THE ORBITON TROUBLESHOOTING BIBLE

## *Every Error, Every Fix, Every Edge Case — Diagnosed and Solved*

> \*\*Version:\*\* 0.7.0 (Tokyo-class)  
> \*\*Last Updated:\*\* 2026-06-08  
> \*\*Purpose:\*\* If something is broken, this document tells you exactly why and exactly how to fix it. No guesswork. No Stack Overflow rabbit holes.

\---

## TABLE OF CONTENTS

2. [The Golden Rule](#1-the-golden-rule)
3. [The Troubleshooter Script](#2-the-troubleshooter-script)
4. [Installation \& Setup Failures](#3-installation--setup-failures)
5. [Python Environment Issues](#3-python-environment-issues)
6. [Import \& Module Errors](#4-import--module-errors)
7. [Microphone \& Voice Recognition](#5-microphone--voice-recognition)
8. [The Self-Listening Bug](#6-the-self-listening-bug)
9. [Text-to-Speech (TTS) Failures](#7-text-to-speech-tts-failures)
10. [Command Failures](#8-command-failures)
11. [File \& Project Issues](#9-file--project-issues)
12. [Math \& Calculation Errors](#10-math--calculation-errors)
13. [Knowledge \& Wikipedia Lookup Failures](#11-knowledge--wikipedia-lookup-failures)
14. [Memory System Issues](#12-memory-system-issues)
15. [Platform-Specific Problems](#13-platform-specific-problems)
16. [Performance \& Lag](#14-performance--lag)
17. [CI/CD \& Testing Failures](#15-cicd--testing-failures)
18. [Development \& Hacking Issues](#16-development--hacking-issues)
19. [The Known Bugs Registry](#17-the-known-bugs-registry)
20. [Emergency Recovery Procedures](#18-emergency-recovery-procedures)
21. [Quick Diagnostic Checklist](#19-quick-diagnostic-checklist)
22. [Where to Get Help](#20-where-to-get-help)

\---

## 1\. The Golden Rule

**Before you do anything else, run this diagnostic:**

```bash
cd Kosmosic-Orbiton
python -c "import sys; print('Python:', sys.version); print('Platform:', sys.platform)"
python -c "import speech\_recognition; print('speech\_recognition: OK')"
python -c "import rich; print('rich: OK')"
python -c "import edge\_tts; print('edge\_tts: OK')"
python -c "from neuro\_link\_intel import get\_intelligence; print('neuro\_link\_intel: OK')"
```

If all five lines print `OK`, your environment is healthy. If any line fails, the fix is in the section matching that module name.

**Second rule:** If voice does not work, **type the command first**. If typing works, the problem is audio/microphone. If typing also fails, the problem is code/dependencies.

**Third rule:** Run `python troubleshooter.py` before reading this manual. It automates most checks and fixes common issues automatically.

\---

## 2\. The Troubleshooter Script

Orbiton ships with a standalone diagnostic tool: `troubleshooter.py`.

### What It Does

* Asks what is broken (won't start, voice fails, TTS silent, etc.)
* Runs automated checks for Python version, dependencies, microphone, internet, files
* Offers to install missing dependencies from `requirements.txt`
* Generates a pre-filled bug report for GitHub issues
* Prints links to `MANUAL.md` and `TROUBLESHOOT.md` (local if available, online fallback)

### How to Run It

```bash
python troubleshooter.py
```

### When to Use It

|Situation|Use Troubleshooter?|
|-|-|
|Orbiton won't start|✅ Yes — checks Python, deps, imports|
|Voice not working|✅ Yes — checks mic, permissions, internet|
|TTS silent|✅ Yes — tests Edge TTS directly, checks audio players|
|Commands wrong|✅ Yes — diagnoses known bugs, tests math engine|
|Files/projects fail|✅ Yes — checks paths, VS Code CLI, aliases|
|Something else|✅ Yes — full system scan with pass/fail report|

### What It Fixes Automatically

* Missing Python modules (offers `pip install -r requirements.txt`)
* Corrupted JSON memory files (offers reset to `{}`)
* Missing `pyaudio` (tells you exact platform command)

### What It Does NOT Fix

* Microphone hardware failures
* OS permission issues (tells you where to go, but doesn't change OS settings)
* Broken source code (tells you to re-clone)

### Generated Bug Report

After any scan, you can generate `orbiton\_bug\_report\_YYYY-MM-DD\_HH-MM-SS.txt` containing:

* OS, Python version, platform
* Pass/fail results for every check
* Pre-filled issue template sections

Paste this directly into a GitHub issue.

\---

## 3\. Installation \& Setup Failures

### Symptom: `git clone` fails with "Repository not found"

**Cause:** Wrong URL, no internet, or Git not installed.  
**Fix:**

```bash
# Verify Git is installed
git --version
# Should print something like "git version 2.40.0"

# If Git is missing:
# Windows: Download from https://git-scm.com/download/win
# macOS: brew install git
# Linux: sudo apt-get install git

# Verify the URL is correct
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
```

### Symptom: `pip install -r requirements.txt` fails with "Could not find a version"

**Cause:** Python version too old, or pip is outdated.  
**Fix:**

```bash
# Check Python version
python --version
# Must be 3.10 or newer. If it says 3.9 or lower, upgrade Python.

# Update pip
python -m pip install --upgrade pip

# Install manually if requirements.txt is missing
pip install speechrecognition edge-tts rich
```

### Symptom: `pip install` fails with "Permission denied"

**Cause:** Trying to install to system Python without admin rights.  
**Fix (pick one):**

```bash
# Option A: Use --user flag
pip install --user -r requirements.txt

# Option B: Use a virtual environment (RECOMMENDED)
python -m venv venv

# Windows:
venv\\Scripts\\activate
pip install -r requirements.txt

# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### Symptom: `pip install speechrecognition` succeeds but `import speech\_recognition` fails

**Cause:** The package name is `speechrecognition` (no underscore) on PyPI, but the import is `speech\_recognition` (with underscore). If you installed a different package with a similar name, it will not import correctly.  
**Fix:**

```bash
pip uninstall speech-recognition  # wrong package
pip uninstall speechrecognition   # reinstall to be safe
pip install speechrecognition
```

### Symptom: `requirements.txt` is missing from the repo

**Cause:** File was accidentally deleted or you are not in the repo root.  
**Fix:**

```bash
# Verify you are in the right directory
ls
# You should see: kosmosic\_orbiton.py, neuro\_link\_intel.py, requirements.txt

# If requirements.txt is truly missing, create it:
cat > requirements.txt << 'EOF'
speechrecognition
edge-tts
rich
EOF
pip install -r requirements.txt
```

\---

## 4\. Python Environment Issues

### Symptom: `python kosmosic\_orbiton.py` opens in Notepad or another app instead of running

**Cause:** On Windows, `python` might not be associated with the Python interpreter. You might have typed the command in PowerShell but Windows thinks it is a file to open.  
**Fix:**

```bash
# Use the full python command
py kosmosic\_orbiton.py

# Or explicitly call python3
python3 kosmosic\_orbiton.py

# Or use the full path
C:\\Users\\You\\AppData\\Local\\Programs\\Python\\Python311\\python.exe kosmosic\_orbiton.py
```

### Symptom: `python` command not found

**Cause:** Python is not in your system PATH.  
**Fix:**

* **Windows:** Reinstall Python and check "Add Python to PATH" during installation.
* **macOS:** `brew install python` or use `python3` instead of `python`.
* **Linux:** `sudo apt-get install python3 python3-pip` and use `python3`.

### Symptom: `ModuleNotFoundError: No module named 'queue'` or `threading`

**Cause:** You are somehow running Python 2, or your Python installation is corrupted.  
**Fix:**

```bash
python --version
# Must say 3.10+ or 3.11+. If it says 2.7, you are using the wrong Python.

# Use python3 explicitly
python3 kosmosic\_orbiton.py
```

### Symptom: `SyntaxError` on the first line of `kosmosic\_orbiton.py`

**Cause:** The file was saved with wrong encoding, or line endings were corrupted (e.g., downloaded as a web page instead of raw code).  
**Fix:**

```bash
# Re-clone the repo fresh
cd ..
rm -rf Kosmosic-Orbiton
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmosic-Orbiton
python kosmosic\_orbiton.py
```

\---

## 5\. Import \& Module Errors

### Symptom: `ImportError: cannot import name 'get\_intelligence' from 'neuro\_link\_intel'`

**Cause:** You are running Orbiton from the wrong directory, or `neuro\_link\_intel.py` is missing/corrupted.  
**Fix:**

```bash
# Verify you are in the repo root
pwd
# Should end with /Kosmosic-Orbiton (or \\Kosmosic-Orbiton on Windows)

# Verify the file exists
ls neuro\_link\_intel.py
# or on Windows: dir neuro\_link\_intel.py

# If missing, re-clone the repo
```

### Symptom: `ModuleNotFoundError: No module named 'rich'`

**Fix:**

```bash
pip install rich
# If using a venv, make sure it is activated first
```

### Symptom: `ModuleNotFoundError: No module named 'edge\_tts'`

**Fix:**

```bash
pip install edge-tts
```

### Symptom: `ModuleNotFoundError: No module named 'speech\_recognition'`

**Fix:**

```bash
pip install speechrecognition
```

### Symptom: `ModuleNotFoundError: No module named 'pyaudio'`

**Cause:** The `speech\_recognition` library sometimes needs `pyaudio` for microphone access, but it is not listed in requirements.txt because it is platform-specific.  
**Fix:**

```bash
# Windows:
pip install pipwin
pipwin install pyaudio

# macOS:
brew install portaudio
pip install pyaudio

# Linux (Ubuntu/Debian):
sudo apt-get install python3-pyaudio
# or
pip install pyaudio

# Linux (Fedora):
sudo dnf install portaudio-devel
pip install pyaudio
```

### Symptom: `ImportError: cannot import name 'NaturalLanguageProcessor'`

**Cause:** `neuro\_link\_intel.py` is an old version or was modified incorrectly.  
**Fix:**

```bash
# Check if the class exists in the file
grep -n "class NaturalLanguageProcessor" neuro\_link\_intel.py
# If no output, your file is corrupted. Re-clone.
```

\---

## 6\. Microphone \& Voice Recognition

### Symptom: Orbiton starts but never seems to hear me

**Step-by-step diagnosis:**

**Step 1: Verify your microphone works at the OS level**

* **Windows:** Settings -> System -> Sound -> Input. Speak and watch the input level bar move.
* **macOS:** System Preferences -> Sound -> Input. Speak and watch the input level.
* **Linux:** Open a terminal and run `arecord -l` to list recording devices. Then test with `arecord -d 5 test.wav` and play it back.

**Step 2: Verify Python can access the microphone**

```python
python -c "
import speech\_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('Say something...')
    audio = r.listen(source, timeout=5)
    print('Got audio!')
"
```

If this hangs at "Say something...", Python cannot access your mic.

**Step 3: Fix microphone permissions**

* **macOS:** System Preferences -> Security \& Privacy -> Privacy -> Microphone -> Check your terminal app (Terminal.app, iTerm2, VS Code terminal, etc.).
* **Windows:** Settings -> Privacy -> Microphone -> "Allow apps to access your microphone" -> ON. Scroll down and allow your terminal app.
* **Linux:** No centralized permission system, but ensure your user is in the `audio` group:

```bash
  sudo usermod -a -G audio $USER
  # Log out and back in for this to take effect
  ```

**Step 4: Check if another app is hogging the microphone**
Close Zoom, Discord, Teams, Skype, or any other app that might be using the microphone. Only one app can usually access the mic at a time.

**Step 5: Try a different microphone**

* Built-in laptop mics are often low quality.
* USB headsets are the most reliable.
* Bluetooth headsets may have latency issues.

### Symptom: Orbiton hears me but recognizes the wrong words

**Cause:** Background noise, unclear speech, or accent mismatch with Google's speech recognition model.  
**Fixes:**

1. **Reduce background noise.** Turn off music, fans, AC.
2. **Speak closer to the microphone.** 6-12 inches is ideal.
3. **Speak clearly but naturally.** Do not whisper. Do not shout.
4. **Use a headset with a boom mic.** This isolates your voice from room noise.
5. **Check your internet connection.** Google Web Speech API requires internet. If offline, speech recognition will fail silently or return gibberish.
6. **Try typing the command instead.** If typing works, the issue is purely speech recognition accuracy, not Orbiton logic.

### Symptom: `AttributeError: 'Recognizer' object has no attribute 'listen'`

**Cause:** You have a conflicting package named `speech\_recognition` that is not the correct library.  
**Fix:**

```bash
pip uninstall speech-recognition
pip uninstall speechrecognition
pip install speechrecognition
```

### Symptom: `OSError: \[Errno -9996] Invalid input device` (Linux)

**Cause:** ALSA cannot find a valid recording device.  
**Fix:**

```bash
# List devices
arecord -l

# If no devices listed, your mic is not detected by ALSA.
# For USB mics, try:
sudo apt-get install alsa-utils

# For PulseAudio systems:
pacmd list-sources | grep name
# Then set the default source:
pacmd set-default-source <your-mic-name>
```

### Symptom: `WaitTimeoutError` after saying "Tokyo"

**Cause:** The speech recognizer timed out waiting for audio. This usually means the microphone is not providing audio data.  
**Fix:** Follow the microphone diagnosis steps above. Most commonly, this is a permissions or hardware issue.

\---

## 7\. The Self-Listening Bug

### Symptom: Orbiton speaks, then immediately triggers a random command (usually a knowledge lookup or search)

**Example:** You say `"Tokyo motivate me"`. Orbiton roasts you. Then it hears its own voice saying the roast and opens a Google search for "deforestation map" or "Bangalore."

**Why it happens:**

1. Orbiton generates TTS output through your speakers.
2. Your microphone picks up the speaker output.
3. The speech recognizer hears the TTS words and interprets them as a new command.
4. Orbiton executes that phantom command.

**This is the #1 most reported bug in Tokyo-class.**

### Immediate Fixes (Do These Now)

**Fix 1: Use headphones or a headset (RECOMMENDED)**
This is the intended design. When audio goes to headphones, the microphone cannot hear it. The bug vanishes completely.

* Any wired headset with a mic works.
* Bluetooth headsets work but may have slight latency.
* Earbuds work fine.

**Fix 2: Lower your speaker volume**
If you must use speakers, turn them down so the mic cannot pick them up. This is unreliable but helps.

**Fix 3: Move the microphone away from the speakers**
Physical separation reduces audio bleed.

**Fix 4: Use a directional microphone**
Cardioid mics (most headset mics) only pick up sound from one direction. Point the mic at your mouth, away from the speakers.

### Technical Workarounds (Advanced)

**Workaround 5: Mute the mic during TTS playback**
There is no built-in mute-during-TTS feature yet, but you can simulate it by adding a sleep delay after TTS:

Edit `kosmosic\_orbiton.py` and find the `speak()` method. Add a small delay after speech:

```python
def speak(self, text: str):
    # ... existing TTS code ...
    time.sleep(0.5)  # Wait half a second after speaking before listening again
```

**Workaround 6: Disable TTS temporarily**
If you only need visual feedback and not voice feedback:

```python
# In kosmosic\_orbiton.py, find the VoiceManager class
# and make speak() return early:
def speak(self, text: str):
    return  # TTS disabled
```

**Workaround 7: Use push-to-talk instead of wake word**
Tokyo-class does not support push-to-talk, but you can approximate it by typing commands instead of using voice when speakers are active.

### Long-Term Fix Status

* **Tokyo-class (current):** No code fix. Use headphones.
* **Odyssey-class (planned):** Will implement audio ducking / echo cancellation.
* **Genesis-class (planned):** Will implement wake-word-only listening after TTS (ignore all audio for 2 seconds after speaking).

\---

## 8\. Text-to-Speech (TTS) Failures

### Symptom: Orbiton executes commands but never speaks

**Diagnosis checklist:**

**Step 1: Is `edge-tts` installed?**

```bash
pip show edge-tts
# If it says "Package(s) not found", install it:
pip install edge-tts
```

**Step 2: Do you have internet?**
Edge TTS downloads voice data from Microsoft servers. It requires an active internet connection.

```bash
# Test connectivity
ping -c 3 speech.platform.bing.com
# or on Windows: ping speech.platform.bing.com
```

If this fails, you are offline. See "Offline TTS Fallback" below.

**Step 3: Are your speakers/headphones working?**
Play a test sound:

* **Windows:** `start "" "C:\\Windows\\Media\\ding.wav"`
* **macOS:** `afplay /System/Library/Sounds/Glass.aiff`
* **Linux:** `paplay /usr/share/sounds/freedesktop/stereo/message.oga`

**Step 4: Is the volume up?**
Check your OS volume mixer. Make sure the terminal app is not muted.

**Step 5: Test Edge TTS directly**

```bash
edge-tts --voice "en-US-AriaNeural" --text "Hello, this is a test" --write-media test.mp3
# Then play test.mp3 with your media player
```

If this works, Edge TTS is fine and the issue is in Orbiton's voice playback logic.

### Symptom: Edge TTS works when tested directly, but Orbiton is silent

**Cause:** Orbiton's voice playback path might be failing. The audio file is generated but not played.  
**Fix:**

Check which playback method your OS is using. Orbiton tries multiple methods:

**Windows playback chain:**

1. Edge TTS generates MP3 -> saved to temp file
2. Orbiton tries to play via `powershell` using `MediaPlayer`
3. Falls back to `startfile` (default app)

**macOS playback chain:**

1. Edge TTS generates MP3
2. Orbiton tries `afplay` (built-in CLI player)
3. Falls back to `open` (default app)

**Linux playback chain:**

1. Edge TTS generates MP3
2. Orbiton tries `mpg123` or `ffplay`
3. Falls back to `xdg-open`

**Fix for Linux:** Install a CLI audio player:

```bash
sudo apt-get install mpg123
# or
sudo apt-get install ffmpeg
```

### Symptom: "Offline fallback is silent" (Linux especially)

**Cause:** When `edge-tts` is installed but the internet is down, Orbiton tries to fall back to system TTS. On Linux, this fallback is `spd-say` (Speech Dispatcher). If `spd-say` is not installed or the speech-dispatcher service is not running, you get silence.  
**Fix:**

```bash
# Install speech dispatcher
sudo apt-get install speech-dispatcher

# Start the service
spd-say "test"
# If you hear nothing, the service may not be running:
speech-dispatcher -d  # start daemon

# If you want to force system TTS and skip Edge TTS entirely:
pip uninstall edge-tts
# Now Orbiton will use system TTS exclusively
```

### Symptom: TTS voice is robotic or low quality

**Cause:** You are using system TTS fallback instead of Edge TTS.  
**Fix:**

```bash
pip install edge-tts
# Ensure you have internet
# Then restart Orbiton
```

### Symptom: TTS is too fast / too slow / wrong accent

**Fix:** Change the voice in CONFIG:

```python
# In kosmosic\_orbiton.py
CONFIG = {
    # ... other keys ...
    "voice": "en-US-JennyNeural",  # Slower, more professional
    # or "en-GB-SoniaNeural" for British accent
    # or "en-AU-NatashaNeural" for Australian
}
```

List all available voices:

```bash
edge-tts --list-voices
```

### Symptom: TTS speaks in a language I do not understand

**Cause:** The voice profile is set to a non-English voice, or the text contains non-ASCII characters that Edge TTS pronounces strangely.  
**Fix:** Set voice to an English profile:

```python
"voice": "en-US-AriaNeural",
```

\---

## 9\. Command Failures

### Symptom: "Tokyo" does not wake Orbiton

**Diagnosis:**

1. Is Orbiton already awake? If it is awake, saying "Tokyo" again does nothing special — it just listens for the next command.
2. Is Orbiton asleep? Say `"wake"` or `"wake up"` first, then try "Tokyo".
3. Is the wake word still "tokyo"? Check if you changed `CONFIG\["wake\_word"]`.
4. Is the speech recognizer hearing "tokyo" as something else? Try typing `tokyo` directly.

**Fix:**

```bash
# Type the wake word to test if the logic works
python kosmosic\_orbiton.py
# Then type: tokyo
# If this works, the issue is speech recognition accuracy
```

### Symptom: `"help"` does nothing

**Status:** Known bug in Tokyo-class. The help handler is not always triggered by voice.  
**Workarounds:**

1. Type `help` instead of saying it.
2. Say it twice.
3. Say `"hell"`, `"halp"`, `"helf"`, or `"elpe"` — these are mapped to help via NLP.
4. If typing `help` also does nothing, check if the `handle\_help` method exists in `kosmosic\_orbiton.py`.

**Permanent fix:** Edit `neuro\_link\_intel.py` and add more homophones for help, or increase the regex priority of the help pattern in `IntentParser.PATTERNS`.

### Symptom: `"exam board"` opens Google instead of exam mode

**Status:** Known bug. The NLP catches `"exambored"` (one word) but `"exam board"` (two words) falls through to the general search intent.  
**Workaround:** Say `"exam mode"` clearly, or say `"exambored"`.  
**Fix:** Edit `neuro\_link\_intel.py` and add to `HOMOPHONES`:

```python
"exam board": "exam mode",
```

### Symptom: `"calculate two times two"` returns an error or wrong answer

**Status:** Fixed in v0.7.0. If you are on an older version, update.  
**Fix:**

```bash
git pull origin main
```

If you are already on v0.6.2+ and it still fails:

1. Check that `MathNormalizer` is imported in `kosmosic\_orbiton.py`:

```python
   from neuro\_link\_intel import get\_intelligence, NaturalLanguageProcessor, MathNormalizer
   ```

2. Check that `handle\_calculate` uses `MathNormalizer`:

```python
   def handle\_calculate(self, expr: str):
       normalized = MathNormalizer.normalize(expr)
       result = MathNormalizer.safe\_eval(normalized)
       self.speak(f"The answer is {result}")
   ```

### Symptom: `"search"` with no query opens a blank page or does nothing

**Expected behavior:** Opening Google homepage with no query is the intended fallback.  
**If it does nothing at all:** Check if `open\_chrome()` is working. See [File \& Project Issues](#9-file--project-issues) for browser opening problems.

### Symptom: `"youtube"` opens YouTube but not the search results

**Cause:** The URL might be malformed if the query contains special characters.  
**Fix:** This is handled by `urllib.parse.quote`. If it fails, check your `quote` import:

```python
from urllib.parse import quote
```

### Symptom: `"weather"` without a city does nothing

**Expected behavior:** If no city is provided, it should search for weather at your location or a default city. If it does nothing, the default city logic might be missing.  
**Workaround:** Always specify a city: `"weather doha"`.

### Symptom: `"track EK215"` opens FlightRadar24 but shows "Flight not found"

**Cause:** FlightRadar24 might not have data for that flight right now, or the flight number format is wrong.  
**Fix:** Verify the flight number. Some airlines use different formats (e.g., `EK215` vs `UAE215`). Try both.

### Symptom: `"metar KJFK"` opens a broken page

**Cause:** The AviationWeather.gov URL format might have changed, or the ICAO code is wrong.  
**Fix:** Verify the ICAO code at https://www.aviationweather.gov/metar. Try `KJFK`, `EGLL`, `OMDB`, etc.

### Symptom: `"clipboard"` says "clipboard is empty" even when it is not

**Cause:** The clipboard library is not detecting your clipboard content, or the content is an image/non-text format.  
**Fix:**

* Ensure you have text (not an image) on the clipboard.
* On Linux, ensure `xclip` or `xsel` is installed:

```bash
  sudo apt-get install xclip xsel
  ```

* On Windows, try copying plain text from Notepad (not from a rich text app).

\---

## 10\. File \& Project Issues

### Symptom: `"open downloads"` says "File not found"

**Cause:** Orbiton is looking for downloads in the wrong place, or the alias is not resolving.  
**Diagnosis:**

**Step 1: Check path resolution**
Orbiton resolves paths in this order:

1. Known aliases (downloads, documents, desktop, pictures, videos, music)
2. Relative to current directory
3. Relative to home directory (`\~`)
4. Absolute path

**Step 2: Find where your Downloads folder actually is**

* **Windows:** `C:\\Users\\<YourName>\\Downloads`
* **macOS:** `/Users/<YourName>/Downloads`
* **Linux:** `/home/<YourName>/Downloads`

**Step 3: Try the absolute path**
Say: `"open C:\\Users\\YourName\\Downloads"` (Windows) or `"open /Users/YourName/Downloads"` (macOS).

**Step 4: Check if the alias is correct**
The alias mapping is hardcoded in `kosmosic\_orbiton.py`. If your OS language is not English, the folder names might be different (e.g., `Téléchargements` on French Windows).  
**Fix:** Use the absolute path, or edit the alias mapping in the source code.

### Symptom: `"open project hex link"` says "Project not found"

**Cause:** The `PROJECTS` dictionary points to `C:\\Projects\\hex-link`, which probably does not exist on your machine.  
**Fix:** Edit `kosmosic\_orbiton.py`:

```python
PROJECTS = {
    "hex link": r"C:\\\\Users\\\\You\\\\Projects\\\\hex-link",  # Change this
    "runway objects": r"C:\\\\Users\\\\You\\\\Projects\\\\runway-objects",
    "udestini": r"C:\\\\Users\\\\You\\\\Projects\\\\udestini",
}
```

### Symptom: `"open project X"` says "code command not found"

**Cause:** VS Code's `code` CLI is not in your system PATH.  
**Fix:**

* **Windows:** Reinstall VS Code and check "Add to PATH" during installation. Or add it manually:

```
  C:\\Users\\<You>\\AppData\\Local\\Programs\\Microsoft VS Code\\bin
  ```

* **macOS:** Open VS Code, press `Cmd+Shift+P`, type "Shell Command: Install 'code' command in PATH", and press Enter.
* **Linux:** Same as macOS, or create a symlink:

```bash
  sudo ln -s /usr/share/code/bin/code /usr/local/bin/code
  ```

### Symptom: `"run myscript.py"` says "File not found"

**Cause:** The script is not in the current directory or home directory.  
**Fix:**

1. Use `go to` to navigate to the folder first:

```
   go to C:\\Users\\You\\Scripts
   run myscript.py
   ```

2. Or use the absolute path:

```
   run C:\\Users\\You\\Scripts\\myscript.py
   ```

### Symptom: `"run myscript.py"` opens in a text editor instead of running

**Cause:** On some systems, `.py` files are associated with a text editor instead of Python. Orbiton uses `python <script>` but if the association is wrong, the OS might open it differently.  
**Fix:** Ensure Python is in your PATH and `.py` files are associated with Python:

* **Windows:** Right-click a `.py` file -> Open with -> Choose Python -> Always use this app.
* Or explicitly run: `python myscript.py` (type this manually to test).

### Symptom: `"latest file"` opens the wrong file

**Cause:** The "latest" logic uses modification time (`mtime`). If a file was touched recently but is not the one you want, it will still be picked.  
**Fix:** Use `"latest file pdf"` to filter by extension, or use `"file search <name>"` to find by partial name.

### Symptom: `"file search report"` returns no results

**Cause:** The search is case-sensitive or only looks in the current directory.  
**Fix:**

1. Navigate to the right directory first: `"go to documents"`
2. Use broader search terms: `"file search rep"` instead of `"file search report"`
3. Check if the file actually exists in that directory.

\---

## 11\. Math \& Calculation Errors

### Symptom: `"calculate 100 / 0"` crashes Orbiton

**Expected behavior:** Should handle gracefully.  
**If it crashes:** The `safe\_eval` function might not be catching `ZeroDivisionError`.  
**Fix:** Update to v0.6.2+ where `safe\_eval` wraps all exceptions:

```python
try:
    result = eval(expr, {"\_\_builtins\_\_": {}}, {})
except Exception as e:
    raise ValueError(f"Math error: {e}")
```

### Symptom: `"calculate two million"` returns "2000000" but "calculate two million five hundred thousand" is wrong

**Cause:** The `words\_to\_number` method handles scale words (`million`, `thousand`, `hundred`) but complex compound numbers might not parse correctly.  
**Workaround:** Break it into simpler expressions:

* `"calculate 2500000"` (type the digits)
* `"calculate two million plus five hundred thousand"`

### Symptom: `"calculate pi times 2"` fails

**Cause:** `safe\_eval` only allows digits and operators. `pi` is not in the whitelist.  
**Workaround:** Use the approximate value:

* `"calculate 3.14159 times 2"`

**Fix for developers:** Add constants to `MathNormalizer`:

```python
# In neuro\_link\_intel.py, add to WORD\_NUMBERS or create a CONSTANTS dict
CONSTANTS = {
    "pi": "3.14159",
    "e": "2.71828",
}
```

### Symptom: `"calculate two to the power of three"` returns wrong result

**Cause:** Multi-word operator replacement order matters. If `"to the power of"` is not replaced before `"power"` is processed as a standalone word, it might break.  
**Fix:** This is handled correctly in v0.6.2+ by sorting operators by length (longest first). If you modified `SPOKEN\_OPS`, ensure `"to the power of"` is before `"power"`.

### Symptom: `calculate` accepts malicious input like `"\_\_import\_\_('os')"`

**Expected behavior:** Should reject it.  
**If it executes:** Your `safe\_eval` whitelist is broken or bypassed.  
**Fix:** Ensure the regex whitelist is strict:

```python
if not re.match(r"^\[0-9+\\-\*/%.()\\s]+$", expr):
    raise ValueError(f"Unsafe characters in expression: {expr}")
```

This must run BEFORE `eval()`.

\---

## 12\. Knowledge \& Wikipedia Lookup Failures

### Symptom: `"tell me about black holes"` says "I don't know anything about that"

**Diagnosis:**

1. **Local knowledge miss:** "black holes" is not in the built-in Space Facts database (it might be under "black hole" singular).
2. **Wikipedia miss:** The Wikipedia REST API might not have a page for that exact term, or the network timed out.

**Fixes:**

1. Try singular form: `"tell me about black hole"`
2. Check your internet connection.
3. Try a different topic: `"tell me about the moon"` (this is in built-in knowledge).
4. Add custom intel:

```bash
   mkdir -p \~/.neuro\_link\_intel
   cat > \~/.neuro\_link\_intel/intel\_astro.json << 'EOF'
   {
     "black holes": "A black hole is a region of spacetime where gravity is so strong that nothing can escape."
   }
   EOF
   ```

   Restart Orbiton.

   ### Symptom: Wikipedia lookup is very slow

   **Cause:** Network latency to `en.wikipedia.org` or DNS resolution issues.  
**Fix:**

   ```bash
# Test Wikipedia API speed
curl -w "@curl-format.txt" -o /dev/null -s "https://en.wikipedia.org/api/rest\_v1/page/summary/Python"
# If it takes >5 seconds, Orbiton will timeout.
```

   **Workaround:** Use local intel files for topics you query frequently. They load instantly.

   ### Symptom: Wikipedia lookup returns gibberish or HTML

   **Cause:** Wikipedia changed their API response format, or the page does not exist and returns an error page.  
**Fix:** Update to the latest version of Orbiton. If the API format changed, the `WikimediaScraper` class needs updating.

   ### Symptom: Cache files grow huge over time

   **Cause:** Every Wikipedia query creates a `.txt` file in `\~/.neuro\_link\_wiki\_cache/`. There is no automatic cleanup.  
**Fix:** Manually clean the cache:

   ```bash
rm -rf \~/.neuro\_link\_wiki\_cache/\*
```

   Or add a cron job to clean it monthly.

   \---

   ## 13\. Memory System Issues

   ### Symptom: `"who am i"` says "I don't know you yet"

   **Cause:** The memory file `\~/.neuro\_link\_memory.json` is empty or missing.  
**Fix:**

   ```bash
# Create the memory file manually
cat > \~/.neuro\_link\_memory.json << 'EOF'
{
  "name": "Your Name",
  "favorite\_language": "Python",
  "location": "Your City"
}
EOF
```

   Restart Orbiton.

   ### Symptom: Memory file is corrupted and Orbiton crashes on startup

   **Cause:** Invalid JSON in the memory file (e.g., you edited it and left a trailing comma).  
**Fix:**

   ```bash
# Validate the JSON
python -m json.tool \~/.neuro\_link\_memory.json
# If it says "Expecting property name enclosed in double quotes", fix the JSON.

# Or reset it completely:
echo '{}' > \~/.neuro\_link\_memory.json
```

   ### Symptom: Orbiton remembers wrong information

   **Cause:** The memory file was edited incorrectly, or multiple users share the same file.  
**Fix:** Edit `\~/.neuro\_link\_memory.json` directly and correct the facts. There is no "forget" command in Tokyo-class.

   \---

   ## 14\. Platform-Specific Problems

   ### Windows

   #### Symptom: `open` commands launch Edge instead of Chrome

   **Cause:** Chrome is not at the expected path, or Chrome is not installed.  
**Fix:**

   ```python
# In kosmosic\_orbiton.py, update CONFIG:
CONFIG = {
    "chrome\_path": {
        "Windows": r"C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
        # If Chrome is installed elsewhere:
        # "Windows": r"C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
    },
    # ...
}
```

   If Chrome is not installed at all, Orbiton falls back to the default browser (usually Edge on Windows 10/11).

   #### Symptom: VS Code projects open but show "Cannot find workspace"

   **Cause:** The project path in `PROJECTS` is wrong, or the folder was moved/deleted.  
**Fix:** Update the path in `PROJECTS` to the actual folder location.

   #### Symptom: TTS fallback uses PowerShell but sounds terrible

   **Expected:** PowerShell TTS (`System.Speech.Synthesis`) is lower quality than Edge TTS. This is normal.  
**Fix:** Get internet access so Edge TTS works, or accept the robotic voice.

   #### Symptom: Headphone detection always returns "No headphones"

   **Cause:** Windows WMI is not detecting your Bluetooth device as an audio endpoint.  
**Fix:** This is a known limitation. Headphone detection is best-effort. It does not affect core functionality — you can still use any microphone.

   ### macOS

   #### Symptom: Terminal says "Microphone access denied" but there is no prompt

   **Cause:** macOS silently denies microphone access if the app was previously denied.  
**Fix:**

1. System Preferences -> Security \& Privacy -> Privacy -> Microphone
2. Find your terminal app (Terminal.app, iTerm2, etc.)
3. Check the box. If it is already checked, uncheck it, recheck it, and restart the terminal.
4. If the terminal is not in the list, run this to force it:

   ```bash
   tccutil reset Microphone
   ```

   Then restart the terminal and try again.

   #### Symptom: `open` commands work but `run` commands fail

   **Cause:** macOS might gate Python script execution with Gatekeeper, especially if the script was downloaded from the internet.  
**Fix:**

   ```bash
# Remove quarantine attributes
xattr -d com.apple.quarantine myscript.py
# Or disable Gatekeeper for that file:
xattr -cr myscript.py
```

   #### Symptom: `afplay` not found

   **Cause:** You are on a very old macOS version, or the command path is different.  
**Fix:** `afplay` is built into macOS and should always be at `/usr/bin/afplay`. If it is missing, your macOS installation is damaged.

   ### Linux

   #### Symptom: `xdg-open` does nothing

   **Cause:** No default browser is set, or `xdg-open` is not installed.  
**Fix:**

   ```bash
# Set default browser
xdg-settings set default-web-browser google-chrome.desktop
# or
xdg-settings set default-web-browser firefox.desktop

# If xdg-open is missing:
sudo apt-get install xdg-utils
```

   #### Symptom: `spd-say` works but Edge TTS is silent

   **Cause:** Edge TTS generates an MP3 but there is no default player to open it.  
**Fix:**

   ```bash
sudo apt-get install mpg123
# or
sudo apt-get install ffmpeg
# or
sudo apt-get install vlc
```

   #### Symptom: `clipboard` command fails with "xclip not found"

   **Fix:**

   ```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
```

   #### Symptom: Orbiton crashes with ALSA/PulseAudio errors

   **Cause:** Linux audio subsystems are complex and often conflict.  
**Fix:**

   ```bash
# Check if PulseAudio is running
pulseaudio --check
# If not running:
pulseaudio --start

# Check ALSA devices
arecord -l
aplay -l

# If using PipeWire (modern Linux):
pactl info
```

   #### Symptom: Permission denied when writing to `\~/.neuro\_link\_memory.json`

   **Cause:** Your home directory permissions are wrong, or the file was created as root.  
**Fix:**

   ```bash
ls -la \~/.neuro\_link\_memory.json
# If it shows root as owner:
sudo chown $USER:$USER \~/.neuro\_link\_memory.json
chmod 644 \~/.neuro\_link\_memory.json
```

   \---

   ## 15\. Performance \& Lag

   ### Symptom: Orbiton takes 3+ seconds to respond to every command

   **Possible causes and fixes:**

   **Cause 1: Slow internet (Edge TTS)**

* **Diagnosis:** Commands that do not involve TTS (like `open`) are fast, but commands with voice output are slow.
* **Fix:** Use typed commands, or disable TTS temporarily. Or get faster internet.

  **Cause 2: Speech recognition latency**

* **Diagnosis:** The delay happens between speaking and seeing the command recognized.
* **Fix:** Google Web Speech API has inherent latency (\~1-2 seconds). This is normal. There is no fix for Tokyo-class.

  **Cause 3: Heavy CPU load**

* **Diagnosis:** Your CPU is at 100% from other apps.
* **Fix:** Close Chrome tabs, stop video rendering, etc.

  **Cause 4: Microphone buffer issues**

* **Diagnosis:** The audio listener is configured with a long timeout.
* **Fix:** Reduce `audio\_timeout` in CONFIG:

  ```python
  "audio\_timeout": 5,  # Instead of 8
  ```

  ### Symptom: Orbiton freezes completely

  **Cause:** Infinite loop, deadlock, or the speech recognition thread is stuck.  
**Fix:**

  ```bash
# Force quit
Ctrl+C

# If that does not work, find the process and kill it
# Windows: Task Manager -> find python.exe -> End Task
# macOS/Linux: ps aux | grep kosmosic\_orbiton
#             kill -9 <PID>
```

  ### Symptom: Orbiton uses 100% CPU

  **Cause:** The audio listener loop is spinning without sleeping.  
**Fix:** This is a bug. Update to the latest version. If it persists, report it with your OS and Python version.

  \---

  ## 16\. CI/CD \& Testing Failures

  ### Symptom: `pytest tests/ -v` fails with `ModuleNotFoundError`

  **Cause:** The tests cannot find `kosmosic\_orbiton.py` because it is not in the Python path.  
**Fix:**

  ```bash
# Ensure you are in the repo root
cd Kosmosic-Orbiton

# Add the current directory to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:."
pytest tests/ -v

# Windows (PowerShell):
$env:PYTHONPATH = "."
pytest tests/ -v
```

  ### Symptom: Tests pass locally but fail on GitHub Actions

  **Cause:** Platform differences. The `launch` tests run on Windows in CI because file operations differ. Other tests run on Ubuntu.  
**Fix:** Check the workflow file (`.github/workflows/<name>.yml`) to see which OS it runs on. If your change is OS-specific, ensure the test mocks the platform correctly.

  ### Symptom: `test\_navigate\_parent` fails with subprocess error

  **Status:** Known flaky test.  
**Fix:** This is already patched in the latest version. Update your repo.

  ### Symptom: Pylint fails with "score too low"

  **Cause:** Your code has style issues (trailing whitespace, missing docstrings, line too long).  
**Fix:**

  ```bash
# Run pylint locally first
pylint kosmosic\_orbiton.py neuro\_link\_intel.py

# Fix the reported issues. Common ones:
# - Trailing whitespace: remove spaces at end of lines
# - Missing docstring: add a one-line docstring to methods
# - Line too long: break lines at 100 characters
```

  ### Symptom: `pytest` shows warnings about invalid escape sequences

  **Cause:** Regex strings in tests or code use `\\` without being raw strings.  
**Fix:** Prefix regex strings with `r`:

  ```python
# Wrong:
pattern = "^calculate\\s+(.+)"
# Right:
pattern = r"^calculate\\s+(.+)"
```

  \---

  ## 17\. Development \& Hacking Issues

  ### Symptom: I added a command but it is never triggered

  **Diagnosis checklist:**

1. Did you add the handler method to `CommandEngine`? (e.g., `handle\_translate`)
2. Did you add the intent pattern to `IntentParser.PATTERNS`?
3. Did you add the routing in `CommandEngine.execute()` or wherever intents are dispatched?
4. Did you restart Orbiton? (Python does not hot-reload.)
5. Did you add tests? (If the intent parser test does not recognize it, the pattern is wrong.)

   ### Symptom: My new command works when typed but not when spoken

   **Cause:** The NLP homophone mapping is missing, or the speech recognizer is hearing something completely different.  
**Fix:**

1. Add the misheard variant to `NaturalLanguageProcessor.HOMOPHONES`.
2. Test what the speech recognizer actually hears by adding debug output:

   ```python
   # In kosmosic\_orbiton.py, temporarily add:
   print(f"DEBUG: Recognized text: {recognized\_text}")
   ```

3. Map whatever it hears to your command.

   ### Symptom: Tests I wrote fail with "engine not found"

   **Cause:** The `engine` fixture is defined in `conftest.py` but your test file is not importing it correctly.  
**Fix:** Ensure your test file is inside the `tests/` directory. `conftest.py` only provides fixtures to tests in the same directory and subdirectories.

   ### Symptom: My PR was rejected for "breaking existing commands"

   **Cause:** Your change modified shared code (like `IntentParser` or `CommandEngine`) and broke backward compatibility.  
**Fix:**

1. Run the full test suite before submitting: `pytest tests/ -v`
2. Test the commands you did NOT modify to ensure they still work.
3. If you modified regex patterns, ensure old patterns still match.

   \---

   ## 18\. The Known Bugs Registry

   This is the official list of all known bugs in Tokyo-class (v0.7) and their status.

|#|Bug|Symptom|Severity|Workaround|Fix Status|
|-|-|-|-|-|-|
|1|**Self-Listening**|TTS triggers phantom commands|High|Use headphones|Planned for Odyssey|
|2|**Help Unresponsive**|"help" voice command fails|Medium|Type `help` instead|Planned for Odyssey|
|3|**Exam Board NLP**|"exam board" triggers search|Low|Say "exambored" or "exam mode"|Fixed in v0.6.2|
|4|**Linux Headphone Detect**|Always returns "No headphones"|Low|None needed; mic still works|Planned for Odyssey|
|5|**Edge TTS Offline Silent**|No sound when offline with edge-tts installed|Medium|Uninstall edge-tts or get internet|Planned for Genesis|
|6|**Hardcoded Windows Paths**|`PROJECTS` dict uses `C:\\Projects\\...`|Low|Edit CONFIG manually|Planned for Genesis|
|7|**Clipboard Non-Text**|"clipboard" fails with image content|Low|Copy text instead|No fix planned|
|8|**Math Complex Numbers**|"calculate i squared" fails|Low|Do not use imaginary numbers|No fix planned|
|9|**TTS Language Mismatch**|Non-English text pronounced badly|Low|Use English only|Planned for Aphrodite|
|10|**Memory No Forget**|Cannot delete a memory fact|Low|Edit JSON manually|Planned for Odyssey|

\---

## 19\. Emergency Recovery Procedures

### Procedure 1: Orbiton is completely frozen

```bash
# Find the Python process
# Windows: Ctrl+Shift+Esc -> Task Manager -> Details -> python.exe -> End Task
# macOS/Linux:
ps aux | grep kosmosic\_orbiton
kill -9 <PID>
```

### Procedure 2: Orbiton config is corrupted beyond repair

```bash
# First, try the troubleshooter
python troubleshooter.py

# If that fails, reset to factory defaults by re-cloning
cd ..
rm -rf Kosmosic-Orbiton
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmosic-Orbiton
pip install -r requirements.txt
```

### Procedure 3: All data files are corrupted

```bash
# Reset all user data
rm -f \~/.neuro\_link\_memory.json
rm -rf \~/.neuro\_link\_wiki\_cache/
rm -rf \~/.neuro\_link\_intel/
# Orbiton will recreate these on next run
```

### Procedure 4: Python environment is completely broken

```bash
# Nuclear option: create a fresh virtual environment
python -m venv fresh\_env

# Windows:
fresh\_env\\Scripts\\activate

# macOS/Linux:
source fresh\_env/bin/activate

# Reinstall everything
pip install speechrecognition edge-tts rich
python kosmosic\_orbiton.py
```

### Procedure 5: Microphone permissions are irrevocably broken (macOS)

```bash
# Reset all microphone permissions
sudo tccutil reset Microphone
# Restart your terminal app
# You will be prompted again for microphone access
```

\---

## 20\. Quick Diagnostic Checklist

Run this checklist in order. Stop when you find the issue.

* \[ ] **Run troubleshooter** (`python troubleshooter.py`)
* \[ ] **Python version is 3.10+** (`python --version`)
* \[ ] **All dependencies installed** (`pip install -r requirements.txt`)
* \[ ] **Running from repo root** (`pwd` ends with `Kosmosic-Orbiton`)
* \[ ] **Can import all modules** (run the Golden Rule diagnostic from Section 1)
* \[ ] **Microphone works at OS level** (input level bar moves when you speak)
* \[ ] **Terminal has microphone permissions** (OS privacy settings)
* \[ ] **No other app is using the microphone** (close Zoom, Discord, etc.)
* \[ ] **Internet works** (for Edge TTS and Wikipedia; not required for core commands)
* \[ ] **Typing commands works** (if typing fails, it is not a mic issue)
* \[ ] **TTS works when tested directly** (`edge-tts` command from Section 7)
* \[ ] **No corrupted data files** (`python -m json.tool \~/.neuro\_link\_memory.json`)
* \[ ] **Tests pass** (`pytest tests/ -v`)

\---

## 21\. Where to Get Help

### If This Document Did Not Solve Your Problem

1. **Run the troubleshooter.** `python troubleshooter.py` automates most checks and generates a bug report.
2. **Check the source code.** The docstrings are decent. Start with `kosmosic\_orbiton.py` -> `CommandEngine`.
3. **Run the tests.** `pytest tests/ -v` will tell you exactly what is broken.
4. **Open an issue** on GitHub: https://github.com/AymanHaidry/Kosmosic-Orbiton/issues

   * Include your OS, Python version, and the exact error message.
   * Include the output of the Golden Rule diagnostic (Section 1).
5. **Check the other docs:**

   * `PHILOSOPHY.md` — Why things are the way they are
   * `ROADMAP.md` — When your bug will be fixed
   * `CONTRIBUTING.md` — How to fix it yourself
   * `TEST\_STATUS.md` — Current CI status

### Before Opening an Issue

**Good bug report:**

```
OS: Windows 11
Python: 3.11.4
Orbiton: 0.7.0
Command: "calculate two times two"
Expected: Speaks "4"
Actual: Crashes with ValueError: Math error: invalid syntax
Steps to reproduce: Fresh install, say "Tokyo calculate two times two"
```

**Bad bug report:**

```
It doesn't work. Fix it.
```

\---

> \*\*"I ran a diagnostic on your life. Critical failure across all sectors."\*\*  
> — Orbiton, on your troubleshooting skills before reading this document

**© 2026 Kosmosic**  
**License:** GNU General Public License v3.0

