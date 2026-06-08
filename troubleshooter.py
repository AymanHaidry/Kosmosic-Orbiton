#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 🔧 ORBITON TROUBLESHOOTER v1.0
 "I ran a diagnostic on your life. Now let me fix your setup."
 Standalone diagnostic tool. Run this when something breaks.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os
import subprocess
import json
import platform
import time
from pathlib import Path
from urllib.parse import quote

# ─── COLORS (no rich dependency — we are the troubleshooter) ──
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    DIM = "\033[2m"

    @classmethod
    def ok(cls, text): return f"{cls.GREEN}✓{cls.RESET} {text}"
    @classmethod
    def fail(cls, text): return f"{cls.RED}✗{cls.RESET} {text}"
    @classmethod
    def warn(cls, text): return f"{cls.YELLOW}⚠{cls.RESET} {text}"
    @classmethod
    def info(cls, text): return f"{cls.BLUE}ℹ{cls.RESET} {text}"
    @classmethod
    def arrow(cls, text): return f"{cls.CYAN}→{cls.RESET} {text}"
    @classmethod
    def title(cls, text): return f"\n{cls.BOLD}{cls.MAGENTA}{text}{cls.RESET}"

def print_banner():
    print(f"""
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
 {Colors.BOLD}🎧 ORBITON TROUBLESHOOTER{Colors.RESET} {Colors.DIM}v0.7 (Tokyo-class){Colors.RESET}
 {Colors.DIM}"I ran a diagnostic on your life. Now let me fix your setup."{Colors.RESET}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}
""")

def ask(prompt, options=None):
    """Ask user for input with optional validation."""
    while True:
        try:
            response = input(f"{Colors.CYAN}>{Colors.RESET} {prompt} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}Interrupted. Exiting.{Colors.RESET}")
            sys.exit(0)
        if options and response not in options:
            print(f"  {Colors.YELLOW}Please enter one of: {', '.join(options)}{Colors.RESET}")
            continue
        return response

def ask_yes_no(prompt, default="y"):
    """Ask a yes/no question."""
    suffix = " [Y/n]" if default == "y" else " [y/N]"
    while True:
        response = ask(prompt + suffix).lower()
        if not response:
            return default == "y"
        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False
        print(f"  {Colors.YELLOW}Please enter y or n.{Colors.RESET}")

def run_cmd(cmd, shell=False, timeout=10, capture=True):
    """Run a shell command safely. Returns (success, stdout, stderr)."""
    try:
        if shell and isinstance(cmd, list):
            cmd = " ".join(cmd)
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except FileNotFoundError:
        return False, "", "Command not found"
    except Exception as e:
        return False, "", str(e)

def check_python_version():
    """Check if Python is 3.10+."""
    version = sys.version_info
    ok = version.major == 3 and version.minor >= 10
    ver_str = f"{version.major}.{version.minor}.{version.micro}"
    if ok:
        print(f"  {Colors.ok(f'Python {ver_str}')} (3.10+ required)")
    else:
        print(f"  {Colors.fail(f'Python {ver_str}')} (3.10+ REQUIRED — you need to upgrade)")
    return ok, ver_str

def check_module(module_name, import_name=None):
    """Check if a Python module is installed."""
    if import_name is None:
        import_name = module_name
    try:
        __import__(import_name)
        print(f"  {Colors.ok(module_name)} installed")
        return True
    except ImportError:
        print(f"  {Colors.fail(module_name)} NOT installed")
        return False

def check_file_exists(filepath, label=None):
    """Check if a file exists."""
    if label is None:
        label = filepath
    path = Path(filepath)
    if path.exists():
        print(f"  {Colors.ok(label)} found at {path}")
        return True
    else:
        print(f"  {Colors.fail(label)} NOT found at {path}")
        return False

def check_internet():
    """Check internet connectivity."""
    ok, _, _ = run_cmd(["ping", "-c", "1", "8.8.8.8"] if sys.platform != "win32" else ["ping", "-n", "1", "8.8.8.8"], timeout=5)
    if ok:
        print(f"  {Colors.ok('Internet')} connection active")
    else:
        print(f"  {Colors.fail('Internet')} connection FAILED (Edge TTS and Wikipedia will not work)")
    return ok

def check_edge_tts_connectivity():
    """Check if Edge TTS servers are reachable."""
    ok, _, _ = run_cmd(["ping", "-c", "1", "speech.platform.bing.com"] if sys.platform != "win32" else ["ping", "-n", "1", "speech.platform.bing.com"], timeout=5)
    if ok:
        print(f"  {Colors.ok('Edge TTS servers')} reachable")
    else:
        print(f"  {Colors.warn('Edge TTS servers')} NOT reachable (offline fallback will be used)")
    return ok

def check_json_file(filepath):
    """Check if a JSON file is valid."""
    path = Path(filepath)
    if not path.exists():
        print(f"  {Colors.warn(filepath)} does not exist (will be created on first use)")
        return True
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"  {Colors.ok(filepath)} valid JSON")
        return True
    except json.JSONDecodeError as e:
        print(f"  {Colors.fail(filepath)} CORRUPTED JSON: {e}")
        return False

def check_microphone_os():
    """Check if OS can see a microphone."""
    plat = sys.platform
    if plat == "win32":
        ok, out, err = run_cmd(
            ['powershell', '-Command', 'Get-PnpDevice -Class AudioEndpoint | Where-Object {$_.Status -eq "OK"} | Select-Object Name'],
            timeout=10
        )
        if ok and "microphone" in out.lower():
            print(f"  {Colors.ok('Microphone')} detected by Windows")
            return True
        else:
            print(f"  {Colors.warn('Microphone')} not clearly detected by Windows (may still work)")
            return None
    elif plat == "darwin":
        ok, out, err = run_cmd(["system_profiler", "SPAudioDataType"], timeout=10)
        if ok and ("microphone" in out.lower() or "input" in out.lower()):
            print(f"  {Colors.ok('Microphone')} detected by macOS")
            return True
        else:
            print(f"  {Colors.warn('Microphone')} not clearly detected by macOS (may still work)")
            return None
    else:
        ok, out, err = run_cmd(["arecord", "-l"], timeout=5)
        if ok and "card" in out.lower():
            print(f"  {Colors.ok('Audio input devices')} detected by ALSA")
            return True
        else:
            print(f"  {Colors.warn('Audio input devices')} not detected by ALSA")
            return False

def check_mic_permissions():
    """Check microphone permissions (best effort per platform)."""
    plat = sys.platform
    if plat == "darwin":
        print(f"  {Colors.warn('macOS mic permissions')} — check System Preferences → Security → Microphone")
        return None
    elif plat == "win32":
        print(f"  {Colors.warn('Windows mic permissions')} — check Settings → Privacy → Microphone")
        return None
    else:
        ok, out, _ = run_cmd(["groups"], timeout=5)
        if ok and "audio" in out:
            print(f"  {Colors.ok('Linux audio group')} user is in 'audio' group")
            return True
        else:
            print(f"  {Colors.warn('Linux audio group')} user NOT in 'audio' group — run: sudo usermod -a -G audio $USER")
            return False

def check_chrome():
    """Check if Chrome is installed."""
    plat = sys.platform
    chrome_paths = {
        "win32": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "linux": "/usr/bin/google-chrome",
    }
    path = chrome_paths.get(plat, chrome_paths["linux"])
    if Path(path).exists():
        print(f"  {Colors.ok('Chrome')} found at {path}")
        return True
    else:
        print(f"  {Colors.warn('Chrome')} NOT found at default path (will use default browser)")
        return False

def check_vs_code():
    """Check if VS Code CLI is available."""
    ok, _, _ = run_cmd(["code", "--version"], timeout=5)
    if ok:
        print(f"  {Colors.ok('VS Code CLI')} ('code' command) available")
        return True
    else:
        print(f"  {Colors.warn('VS Code CLI')} NOT available — 'open project' commands will fail")
        return False

def check_pyaudio():
    """Check if pyaudio is available."""
    try:
        import pyaudio
        print(f"  {Colors.ok('PyAudio')} installed")
        return True
    except ImportError:
        print(f"  {Colors.warn('PyAudio')} NOT installed (speech recognition may fail on some platforms)")
        return False

def install_module(module_name, pip_name=None):
    """Offer to install a missing module."""
    if pip_name is None:
        pip_name = module_name
    print(f"\n  {Colors.YELLOW}Module '{module_name}' is missing.{Colors.RESET}")
    if ask_yes_no(f"Install {pip_name} now?"):
        print(f"  {Colors.CYAN}Running: pip install {pip_name}{Colors.RESET}")
        ok, out, err = run_cmd([sys.executable, "-m", "pip", "install", pip_name], timeout=60)
        if ok:
            print(f"  {Colors.ok(f'{pip_name} installed successfully')}")
            return True
        else:
            print(f"  {Colors.fail(f'Installation failed: {err}')}")
            print(f"  {Colors.YELLOW}Try running manually:{Colors.RESET} pip install {pip_name}")
            return False
    return False

def install_from_requirements():
    """Offer to install ALL dependencies from requirements.txt."""
    req_path = Path("requirements.txt")
    if not req_path.exists():
        print(f"\n  {Colors.warn('requirements.txt not found')} in current directory.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Make sure you are in the Kosmosic-Orbiton repo root.")
        return False

    print(f"\n  {Colors.YELLOW}Multiple dependencies missing.{Colors.RESET}")
    print(f"  {Colors.CYAN}→{Colors.RESET} Found requirements.txt with these packages:")
    try:
        with open(req_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        for line in lines:
            print(f"     {Colors.DIM}- {line}{Colors.RESET}")
    except Exception:
        pass

    if ask_yes_no("Install ALL dependencies from requirements.txt now?"):
        print(f"  {Colors.CYAN}Running: pip install -r requirements.txt{Colors.RESET}")
        ok, out, err = run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], timeout=120)
        if ok:
            print(f"  {Colors.ok('All dependencies installed successfully')}")
            return True
        else:
            print(f"  {Colors.fail(f'Installation failed: {err}')}")
            print(f"  {Colors.YELLOW}Try running manually:{Colors.RESET} pip install -r requirements.txt")
            return False
    return False

def fix_corrupted_json(filepath):
    """Offer to fix a corrupted JSON file."""
    print(f"\n  {Colors.YELLOW}File {filepath} has corrupted JSON.{Colors.RESET}")
    if ask_yes_no("Reset it to empty {}?"):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({}, f)
            print(f"  {Colors.ok(f'{filepath} reset to empty JSON')}")
            return True
        except Exception as e:
            print(f"  {Colors.fail(f'Could not reset: {e}')}")
            return False
    return False

def get_docs_url(local_path, online_url):
    """Return the best available docs URL."""
    if Path(local_path).exists():
        return f"file://{Path(local_path).resolve()}"
    return online_url

def print_docs_links():
    """Print links to documentation."""
    manual_local = "docs/MANUAL.md"
    manual_online = "https://github.com/AymanHaidry/Kosmosic-Orbiton/blob/main/docs/MANUAL.md"
    troubleshoot_local = "docs/TROUBLESHOOT.md"
    troubleshoot_online = "https://github.com/AymanHaidry/Kosmosic-Orbiton/blob/main/docs/TROUBLESHOOT.md"

    manual_url = get_docs_url(manual_local, manual_online)
    troubleshoot_url = get_docs_url(troubleshoot_local, troubleshoot_online)

    print(f"\n  {Colors.BOLD}Documentation:{Colors.RESET}")
    print(f"    {Colors.CYAN}→{Colors.RESET} Manual: {Colors.BLUE}{manual_url}{Colors.RESET}")
    print(f"    {Colors.CYAN}→{Colors.RESET} Troubleshooting: {Colors.BLUE}{troubleshoot_url}{Colors.RESET}")

def generate_bug_report(results):
    """Generate a bug report file and pause so user can see it."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"orbiton_bug_report_{timestamp}.txt"

    report = f"""ORBITON BUG REPORT
Generated by Troubleshooter v0.7
Date: {time.strftime("%Y-%m-%d %H:%M:%S")}

=== SYSTEM INFO ===
OS: {platform.system()} {platform.release()}
Platform: {sys.platform}
Python: {sys.version}
Python executable: {sys.executable}
Working directory: {os.getcwd()}

=== DIAGNOSTIC RESULTS ===
"""
    for key, value in results.items():
        status = "PASS" if value else "FAIL"
        report += f"{key}: {status}\n"

    report += """
=== PLEASE DESCRIBE YOUR ISSUE BELOW ===
(What command did you run? What did you expect? What happened instead?)


=== STEPS TO REPRODUCE ===
1. 
2. 
3. 

=== ADDITIONAL CONTEXT ===
(Any error messages, screenshots, or other info)

"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n  {Colors.ok(f'Bug report saved to: {filename}')}")
    print(f"  {Colors.CYAN}→{Colors.RESET} Paste this into a GitHub issue:")
    print(f"     {Colors.BLUE}https://github.com/AymanHaidry/Kosmosic-Orbiton/issues{Colors.RESET}")
    print_docs_links()

    # PAUSE so terminal doesn't close
    print(f"\n  {Colors.DIM}Press Enter to continue...{Colors.RESET}")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass

    return filename

# ─── MAIN TROUBLESHOOTING FLOWS ──────────────────────────────

def flow_wont_start():
    """Orbiton won't start at all."""
    print(Colors.title("DIAGNOSING: Orbiton won't start"))

    results = {}

    # Check 1: Python version
    print(f"\n{Colors.BOLD}Checking Python...{Colors.RESET}")
    ok, ver = check_python_version()
    results["python_version"] = ok
    if not ok:
        print(f"\n  {Colors.RED}FATAL:{Colors.RESET} You need Python 3.10 or newer.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Download from https://python.org/downloads/")
        print(f"  {Colors.CYAN}→{Colors.RESET} On macOS: brew install python@3.11")
        print(f"  {Colors.CYAN}→{Colors.RESET} On Ubuntu: sudo apt-get install python3.11")
        print_docs_links()
        return results

    # Check 2: We are in the right directory
    print(f"\n{Colors.BOLD}Checking working directory...{Colors.RESET}")
    if not check_file_exists("kosmosic_orbiton.py", "Main file (kosmosic_orbiton.py)"):
        results["in_repo"] = False
        print(f"\n  {Colors.RED}FATAL:{Colors.RESET} You are not in the Kosmosic-Orbiton directory.")
        print(f"  {Colors.CYAN}→{Colors.RESET} cd into the repo folder:")
        print(f"     cd Kosmosic-Orbiton")
        print(f"     python kosmosic_orbiton.py")
        print_docs_links()
        return results
    results["in_repo"] = True

    # Check 3: Core dependencies
    print(f"\n{Colors.BOLD}Checking dependencies...{Colors.RESET}")
    results["speech_recognition"] = check_module("speechrecognition", "speech_recognition")
    results["rich"] = check_module("rich")
    results["edge_tts"] = check_module("edge-tts", "edge_tts")

    missing = [k for k, v in results.items() if k in ("speech_recognition", "rich", "edge_tts") and not v]
    if missing:
        print(f"\n  {Colors.YELLOW}Missing dependencies detected.{Colors.RESET}")
        # Offer requirements.txt install first
        if Path("requirements.txt").exists():
            if install_from_requirements():
                # Re-check
                print(f"\n{Colors.BOLD}Re-checking dependencies...{Colors.RESET}")
                results["speech_recognition"] = check_module("speechrecognition", "speech_recognition")
                results["rich"] = check_module("rich")
                results["edge_tts"] = check_module("edge-tts", "edge_tts")
            else:
                # Fall back to individual installs
                for mod in missing:
                    pip_name = "speechrecognition" if mod == "speech_recognition" else mod
                    install_module(mod, pip_name)
        else:
            # No requirements.txt — individual installs
            for mod in missing:
                pip_name = "speechrecognition" if mod == "speech_recognition" else mod
                install_module(mod, pip_name)

    # Check 4: neuro_link_intel.py exists and imports
    print(f"\n{Colors.BOLD}Checking intelligence module...{Colors.RESET}")
    results["neuro_link_intel"] = check_file_exists("neuro_link_intel.py")
    if results["neuro_link_intel"]:
        try:
            from neuro_link_intel import get_intelligence, NaturalLanguageProcessor, MathNormalizer
            print(f"  {Colors.ok('neuro_link_intel')} imports successfully")
            results["neuro_link_intel_import"] = True
        except Exception as e:
            print(f"  {Colors.fail('neuro_link_intel')} import FAILED: {e}")
            results["neuro_link_intel_import"] = False
            print(f"\n  {Colors.RED}FATAL:{Colors.RESET} The intelligence module is corrupted.")
            print(f"  {Colors.CYAN}→{Colors.RESET} Re-clone the repo:")
            print(f"     cd ..")
            print(f"     rm -rf Kosmosic-Orbiton")
            print(f"     git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git")

    # Check 5: Try to actually run it
    print(f"\n{Colors.BOLD}Attempting to start Orbiton...{Colors.RESET}")
    print(f"  {Colors.DIM}(This will run for 3 seconds then auto-kill){Colors.RESET}")
    ok, out, err = run_cmd([sys.executable, "kosmosic_orbiton.py"], timeout=3)
    if ok or "tokyo" in out.lower() or "loading" in out.lower() or "ready" in out.lower():
        print(f"  {Colors.ok('Orbiton starts')} (killed after 3s to prevent hanging)")
        results["starts"] = True
    else:
        print(f"  {Colors.fail('Orbiton failed to start')}")
        if err:
            print(f"  {Colors.RED}Error output:{Colors.RESET}")
            for line in err.strip().split("\n")[:10]:
                print(f"    {Colors.DIM}{line}{Colors.RESET}")
        results["starts"] = False

    print_docs_links()
    return results

def flow_voice_not_working():
    """Voice commands don't work."""
    print(Colors.title("DIAGNOSING: Voice commands don't work"))

    results = {}

    # Check 1: Does typing work?
    print(f"\n{Colors.BOLD}First: Does typing commands work?{Colors.RESET}")
    print(f"  {Colors.CYAN}→{Colors.RESET} Run: python kosmosic_orbiton.py")
    print(f"  {Colors.CYAN}→{Colors.RESET} Type: what time is it")
    print(f"  {Colors.CYAN}→{Colors.RESET} Press Enter")
    typed_works = ask_yes_no("Did Orbiton respond correctly?")
    results["typing_works"] = typed_works

    if not typed_works:
        print(f"\n  {Colors.RED}If typing doesn't work, voice won't either.{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Run the 'Orbiton won't start' troubleshooter first.")
        print_docs_links()
        return results

    # Check 2: Microphone hardware
    print(f"\n{Colors.BOLD}Checking microphone hardware...{Colors.RESET}")
    results["mic_os"] = check_microphone_os()

    # Check 3: Microphone permissions
    print(f"\n{Colors.BOLD}Checking microphone permissions...{Colors.RESET}")
    results["mic_perms"] = check_mic_permissions()

    # Check 4: PyAudio
    print(f"\n{Colors.BOLD}Checking PyAudio...{Colors.RESET}")
    results["pyaudio"] = check_pyaudio()
    if not results["pyaudio"]:
        if sys.platform == "linux":
            print(f"\n  {Colors.CYAN}→{Colors.RESET} Linux: sudo apt-get install python3-pyaudio")
        elif sys.platform == "darwin":
            print(f"\n  {Colors.CYAN}→{Colors.RESET} macOS: brew install portaudio && pip install pyaudio")
        elif sys.platform == "win32":
            print(f"\n  {Colors.CYAN}→{Colors.RESET} Windows: pip install pipwin && pipwin install pyaudio")

    # Check 5: Internet (for Google speech recognition)
    print(f"\n{Colors.BOLD}Checking internet...{Colors.RESET}")
    results["internet"] = check_internet()
    if not results["internet"]:
        print(f"\n  {Colors.YELLOW}Google Web Speech API requires internet.{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Voice recognition will not work offline.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Use typed commands instead, or connect to internet.")

    # Check 6: Self-listening
    print(f"\n{Colors.BOLD}Checking for self-listening...{Colors.RESET}")
    print(f"  {Colors.CYAN}→{Colors.RESET} Are you using speakers (not headphones)?")
    using_speakers = ask_yes_no("Are you using speakers?")
    if using_speakers:
        print(f"\n  {Colors.YELLOW}SELF-LISTENING BUG DETECTED.{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Use headphones/headset. This is the #1 cause of phantom commands.")
        print(f"  {Colors.CYAN}→{Colors.RESET} If you must use speakers, lower volume and move mic away.")
        results["self_listening"] = True
    else:
        results["self_listening"] = False

    # Summary
    print(f"\n{Colors.BOLD}SUMMARY:{Colors.RESET}")
    if results.get("mic_os") and results.get("mic_perms") and results.get("internet") and not results.get("self_listening"):
        print(f"  {Colors.GREEN}All checks passed. Voice should work.{Colors.RESET}")
        print(f"  {Colors.YELLOW}If it still doesn't work, try:{Colors.RESET}")
        print(f"    1. Speak more clearly")
        print(f"    2. Reduce background noise")
        print(f"    3. Move closer to the microphone")
    else:
        print(f"  {Colors.YELLOW}Issues found. Apply the fixes above and try again.{Colors.RESET}")

    print_docs_links()
    return results

def flow_tts_silent():
    """Orbiton executes commands but never speaks."""
    print(Colors.title("DIAGNOSING: Orbiton doesn't speak (TTS silent)"))

    results = {}

    # Check 1: Edge TTS installed
    print(f"\n{Colors.BOLD}Checking Edge TTS...{Colors.RESET}")
    results["edge_tts"] = check_module("edge-tts", "edge_tts")
    if not results["edge_tts"]:
        if Path("requirements.txt").exists():
            install_from_requirements()
        else:
            install_module("edge-tts", "edge-tts")
        results["edge_tts"] = check_module("edge-tts", "edge_tts")

    # Check 2: Internet
    print(f"\n{Colors.BOLD}Checking internet...{Colors.RESET}")
    results["internet"] = check_internet()
    results["edge_tts_online"] = check_edge_tts_connectivity()

    if not results["internet"]:
        print(f"\n  {Colors.YELLOW}You are offline. Edge TTS requires internet.{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Options:")
        print(f"     1. Connect to internet (recommended)")
        print(f"     2. Uninstall edge-tts to force system TTS fallback:")
        print(f"        pip uninstall edge-tts")
        print(f"     3. Accept silence — core commands still work")

    # Check 3: Speakers/headphones
    print(f"\n{Colors.BOLD}Checking audio output...{Colors.RESET}")
    print(f"  {Colors.CYAN}→{Colors.RESET} Are your speakers/headphones plugged in and turned up?")

    # Check 4: Test Edge TTS directly
    if results.get("edge_tts") and results.get("internet"):
        print(f"\n{Colors.BOLD}Testing Edge TTS directly...{Colors.RESET}")
        print(f"  {Colors.DIM}Generating test audio...{Colors.RESET}")
        ok, _, err = run_cmd(
            ["edge-tts", "--voice", "en-US-AriaNeural", "--text", "Hello, this is Orbiton", "--write-media", "troubleshooter_test.mp3"],
            timeout=15
        )
        if ok and Path("troubleshooter_test.mp3").exists():
            print(f"  {Colors.ok('Edge TTS')} generates audio successfully")
            results["edge_tts_direct"] = True

            # Try to play it
            plat = sys.platform
            if plat == "win32":
                play_cmd = ["start", "", "troubleshooter_test.mp3"]
                shell = True
            elif plat == "darwin":
                play_cmd = ["afplay", "troubleshooter_test.mp3"]
                shell = False
            else:
                # Try multiple Linux players
                for player in ["mpg123", "ffplay", "vlc", "xdg-open"]:
                    ok2, _, _ = run_cmd([player, "troubleshooter_test.mp3"], timeout=5)
                    if ok2:
                        print(f"  {Colors.ok('Audio player')} '{player}' works")
                        results["audio_player"] = player
                        break
                else:
                    print(f"  {Colors.fail('No audio player')} found")
                    print(f"  {Colors.CYAN}→{Colors.RESET} Install one: sudo apt-get install mpg123")
                    results["audio_player"] = None
                # Clean up
                try:
                    Path("troubleshooter_test.mp3").unlink()
                except:
                    pass
                print_docs_links()
                return results

            if plat in ("win32", "darwin"):
                ok2, _, _ = run_cmd(play_cmd, shell=shell, timeout=10)
                if ok2:
                    print(f"  {Colors.ok('Audio playback')} works")
                    results["audio_playback"] = True
                else:
                    print(f"  {Colors.fail('Audio playback')} failed")
                    results["audio_playback"] = False

                # Clean up
                try:
                    Path("troubleshooter_test.mp3").unlink()
                except:
                    pass
        else:
            print(f"  {Colors.fail('Edge TTS direct test')} failed: {err}")
            results["edge_tts_direct"] = False

    print_docs_links()
    return results

def flow_commands_wrong():
    """Commands do the wrong thing or don't execute."""
    print(Colors.title("DIAGNOSING: Commands do the wrong thing"))

    results = {}

    print(f"\n{Colors.BOLD}Which command is broken?{Colors.RESET}")
    print(f"  [1] 'help' does nothing")
    print(f"  [2] 'exam mode' opens search instead")
    print(f"  [3] 'calculate' gives wrong answers")
    print(f"  [4] 'open project' fails")
    print(f"  [5] 'clipboard' is empty")
    print(f"  [6] Other command")

    choice = ask("Enter number:", ["1", "2", "3", "4", "5", "6"])

    if choice == "1":
        print(f"\n  {Colors.YELLOW}KNOWN BUG:{Colors.RESET} 'help' voice command is unreliable in Tokyo-class.")
        print(f"  {Colors.CYAN}→{Colors.RESET} WORKAROUND: Type 'help' instead of saying it.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Try saying 'hell', 'halp', 'helf', or 'elpe' (NLP homophones).")
        print(f"  {Colors.CYAN}→{Colors.RESET} Say it twice.")
        print(f"\n  {Colors.DIM}Fix planned for Odyssey-class.{Colors.RESET}")
        results["issue"] = "help_unresponsive"

    elif choice == "2":
        print(f"\n  {Colors.YELLOW}KNOWN BUG:{Colors.RESET} 'exam board' (two words) falls through to search.")
        print(f"  {Colors.CYAN}→{Colors.RESET} WORKAROUND: Say 'exam mode' clearly, or 'exambored'.")
        print(f"\n  {Colors.DIM}Fix planned for Odyssey-class.{Colors.RESET}")
        results["issue"] = "exam_board_nlp"

    elif choice == "3":
        print(f"\n{Colors.BOLD}Checking calculate command...{Colors.RESET}")
        try:
            from neuro_link_intel import MathNormalizer
            test_cases = [
                ("two times two", "4"),
                ("twenty five divided by five", "5.0"),
                ("three squared", "9"),
                ("100 mod 7", "2"),
            ]
            all_pass = True
            for spoken, expected in test_cases:
                normalized = MathNormalizer.normalize(spoken)
                result = MathNormalizer.safe_eval(normalized)
                ok = result == expected or (expected in result)
                status = Colors.ok(f"'{spoken}' -> {result}") if ok else Colors.fail(f"'{spoken}' -> {result} (expected {expected})")
                print(f"    {status}")
                if not ok:
                    all_pass = False
            results["math_tests"] = all_pass
            if all_pass:
                print(f"\n  {Colors.GREEN}Math engine is working correctly.{Colors.RESET}")
                print(f"  {Colors.YELLOW}If your specific expression failed, it may not be supported.{Colors.RESET}")
            else:
                print(f"\n  {Colors.RED}Math engine has issues. Update to latest version:{Colors.RESET}")
                print(f"  {Colors.CYAN}→{Colors.RESET} git pull origin main")
        except Exception as e:
            print(f"  {Colors.fail(f'Math engine test failed: {e}')}")
            results["math_tests"] = False

    elif choice == "4":
        print(f"\n{Colors.BOLD}Checking VS Code and project paths...{Colors.RESET}")
        results["vs_code"] = check_vs_code()

        # Check PROJECTS dict
        try:
            import kosmosic_orbiton as ko
            projects = ko.PROJECTS if hasattr(ko, 'PROJECTS') else {}
            if projects:
                print(f"\n  {Colors.BOLD}Configured projects:{Colors.RESET}")
                for name, path in projects.items():
                    exists = Path(path).exists()
                    status = Colors.ok(f"'{name}' -> {path}") if exists else Colors.fail(f"'{name}' -> {path} (NOT FOUND)")
                    print(f"    {status}")
            else:
                print(f"  {Colors.warn('No projects configured')}")
        except Exception as e:
            print(f"  {Colors.warn(f'Could not read PROJECTS dict: {e}')}")

        print(f"\n  {Colors.CYAN}→{Colors.RESET} To fix: Edit PROJECTS in kosmosic_orbiton.py to point to actual folders.")

    elif choice == "5":
        print(f"\n{Colors.BOLD}Checking clipboard...{Colors.RESET}")
        plat = sys.platform
        if plat == "linux":
            ok, _, _ = run_cmd(["which", "xclip"], timeout=5)
            if ok:
                print(f"  {Colors.ok('xclip')} installed")
            else:
                ok2, _, _ = run_cmd(["which", "xsel"], timeout=5)
                if ok2:
                    print(f"  {Colors.ok('xsel')} installed")
                else:
                    print(f"  {Colors.fail('Neither xclip nor xsel')} installed")
                    print(f"  {Colors.CYAN}→{Colors.RESET} sudo apt-get install xclip")

        print(f"\n  {Colors.CYAN}→{Colors.RESET} Make sure you have TEXT (not an image) on the clipboard.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Try copying from Notepad instead of a rich text app.")
        results["issue"] = "clipboard"

    elif choice == "6":
        print(f"\n  {Colors.YELLOW}Please describe the issue in a GitHub issue:{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} https://github.com/AymanHaidry/Kosmosic-Orbiton/issues")
        print_docs_links()
        results["issue"] = "other"

    return results

def flow_files_projects():
    """File and project commands fail."""
    print(Colors.title("DIAGNOSING: File & project commands fail"))

    results = {}

    print(f"\n{Colors.BOLD}Which file command is broken?{Colors.RESET}")
    print(f"  [1] 'open <folder>' doesn't open anything")
    print(f"  [2] 'open project <name>' fails")
    print(f"  [3] 'run <script>' fails")
    print(f"  [4] 'go to <folder>' doesn't change directory")

    choice = ask("Enter number:", ["1", "2", "3", "4"])

    if choice == "1":
        print(f"\n{Colors.BOLD}Checking path resolution...{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Orbiton resolves paths in this order:")
        print(f"     1. Known aliases (downloads, documents, desktop, etc.)")
        print(f"     2. Relative to current directory")
        print(f"     3. Relative to home directory (~)")
        print(f"     4. Absolute path")

        # Check known aliases
        home = Path.home()
        aliases = {
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "desktop": home / "Desktop",
            "pictures": home / "Pictures",
            "videos": home / "Videos",
            "music": home / "Music",
        }
        print(f"\n  {Colors.BOLD}Checking known folder aliases:{Colors.RESET}")
        for alias, path in aliases.items():
            exists = path.exists()
            status = Colors.ok(f"{alias}: {path}") if exists else Colors.fail(f"{alias}: {path} (NOT FOUND)")
            print(f"    {status}")

        print(f"\n  {Colors.CYAN}→{Colors.RESET} If your OS language is not English, folder names may differ.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Use absolute paths: 'open C:\\\\Users\\\\You\\\\Downloads'")

    elif choice == "2":
        return flow_commands_wrong()  # Reuse the project logic

    elif choice == "3":
        print(f"\n{Colors.BOLD}Checking script execution...{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} Ensure the script exists in current dir or home dir.")
        print(f"  {Colors.CYAN}→{Colors.RESET} Use 'go to' to navigate to the script's folder first.")
        print(f"  {Colors.CYAN}→{Colors.RESET} On macOS, Gatekeeper may block scripts. Run:")
        print(f"     xattr -d com.apple.quarantine myscript.py")

    elif choice == "4":
        print(f"\n{Colors.BOLD}Checking directory navigation...{Colors.RESET}")
        print(f"  {Colors.CYAN}→{Colors.RESET} 'go to parent' goes up one level (cd ..)")
        print(f"  {Colors.CYAN}→{Colors.RESET} 'go to back' goes to previous directory")
        print(f"  {Colors.CYAN}→{Colors.RESET} Other names are resolved as folder names")

    print_docs_links()
    return results

def flow_other():
    """Something else is broken."""
    print(Colors.title("DIAGNOSING: Something else"))

    print(f"\n{Colors.BOLD}Running full system scan...{Colors.RESET}")

    results = {}

    # Comprehensive scan
    print(f"\n{Colors.BOLD}Python & Environment:{Colors.RESET}")
    ok, ver = check_python_version()
    results["python_version"] = ok

    print(f"\n{Colors.BOLD}Dependencies:{Colors.RESET}")
    results["speech_recognition"] = check_module("speechrecognition", "speech_recognition")
    results["rich"] = check_module("rich")
    results["edge_tts"] = check_module("edge-tts", "edge_tts")
    results["pyaudio"] = check_pyaudio()

    # Auto-install missing deps from requirements.txt
    missing_deps = [k for k, v in results.items() if k in ("speech_recognition", "rich", "edge_tts") and not v]
    if missing_deps and Path("requirements.txt").exists():
        print(f"\n  {Colors.YELLOW}Missing dependencies detected.{Colors.RESET}")
        if install_from_requirements():
            # Re-check
            print(f"\n{Colors.BOLD}Re-checking dependencies...{Colors.RESET}")
            results["speech_recognition"] = check_module("speechrecognition", "speech_recognition")
            results["rich"] = check_module("rich")
            results["edge_tts"] = check_module("edge-tts", "edge_tts")

    print(f"\n{Colors.BOLD}Files:{Colors.RESET}")
    results["main_file"] = check_file_exists("kosmosic_orbiton.py")
    results["intel_file"] = check_file_exists("neuro_link_intel.py")

    print(f"\n{Colors.BOLD}Data Files:{Colors.RESET}")
    home = Path.home()
    results["memory_json"] = check_json_file(home / ".neuro_link_memory.json")
    results["wiki_cache"] = check_file_exists(home / ".neuro_link_wiki_cache", "Wiki cache dir")
    results["intel_dir"] = check_file_exists(home / ".neuro_link_intel", "Intel dir")

    print(f"\n{Colors.BOLD}Network:{Colors.RESET}")
    results["internet"] = check_internet()
    results["edge_tts_online"] = check_edge_tts_connectivity()

    print(f"\n{Colors.BOLD}System:{Colors.RESET}")
    results["chrome"] = check_chrome()
    results["vs_code"] = check_vs_code()
    results["mic_os"] = check_microphone_os()

    # Count issues
    failures = [k for k, v in results.items() if v is False]
    warnings = [k for k, v in results.items() if v is None]

    print(f"\n{Colors.BOLD}SCAN COMPLETE:{Colors.RESET}")
    print(f"  {Colors.GREEN if not failures else Colors.RED}{len(failures)} failures{Colors.RESET}")
    print(f"  {Colors.YELLOW}{len(warnings)} warnings{Colors.RESET}")

    if failures:
        print(f"\n  {Colors.RED}Issues found:{Colors.RESET}")
        for f in failures:
            print(f"    {Colors.fail(f)}")

    print_docs_links()
    return results

# ─── MAIN MENU ────────────────────────────────────────────────

def main():
    print_banner()

    print(f"{Colors.BOLD}What is broken?{Colors.RESET}")
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Orbiton won't start at all")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Voice commands don't work")
    print(f"  {Colors.CYAN}[3]{Colors.RESET} Orbiton doesn't speak (TTS silent)")
    print(f"  {Colors.CYAN}[4]{Colors.RESET} Commands do the wrong thing")
    print(f"  {Colors.CYAN}[5]{Colors.RESET} File/project commands fail")
    print(f"  {Colors.CYAN}[6]{Colors.RESET} Something else / full system scan")
    print(f"  {Colors.CYAN}[7]{Colors.RESET} Generate bug report from last scan")
    print(f"  {Colors.CYAN}[q]{Colors.RESET} Quit")

    choice = ask("Enter number:", ["1", "2", "3", "4", "5", "6", "7", "q"])

    if choice == "q":
        print(f"\n{Colors.DIM}Stay productive. Or don't. I don't care.{Colors.RESET}")
        # PAUSE so terminal doesn't close
        print(f"\n  {Colors.DIM}Press Enter to exit...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        return

    results = {}

    if choice == "1":
        results = flow_wont_start()
    elif choice == "2":
        results = flow_voice_not_working()
    elif choice == "3":
        results = flow_tts_silent()
    elif choice == "4":
        results = flow_commands_wrong()
    elif choice == "5":
        results = flow_files_projects()
    elif choice == "6":
        results = flow_other()
    elif choice == "7":
        print(f"\n{Colors.YELLOW}No previous scan data in this session.{Colors.RESET}")
        print(f"{Colors.CYAN}→{Colors.RESET} Run a scan first (options 1-6), then come back.")
        # PAUSE
        print(f"\n  {Colors.DIM}Press Enter to continue...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        return

    # Post-flow options
    print(f"\n{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"{Colors.BOLD}What now?{Colors.RESET}")
    print(f"  {Colors.CYAN}[1]{Colors.RESET} Run another troubleshooter")
    print(f"  {Colors.CYAN}[2]{Colors.RESET} Generate bug report")
    print(f"  {Colors.CYAN}[3]{Colors.RESET} Run full system scan")
    print(f"  {Colors.CYAN}[q]{Colors.RESET} Quit")

    next_choice = ask("Enter number:", ["1", "2", "3", "q"])

    if next_choice == "1":
        main()  # Recurse
    elif next_choice == "2":
        generate_bug_report(results)
        # generate_bug_report already pauses
    elif next_choice == "3":
        flow_other()
        # After flow_other, also pause
        print(f"\n  {Colors.DIM}Press Enter to continue...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
    elif next_choice == "q":
        print(f"\n{Colors.DIM}Your ancestors built empires. You cannot even close 3 Chrome tabs.{Colors.RESET}")
        # PAUSE so terminal doesn't close
        print(f"\n  {Colors.DIM}Press Enter to exit...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted. Exiting.{Colors.RESET}")
        # PAUSE
        print(f"\n  {Colors.DIM}Press Enter to exit...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}TROUBLESHOOTER CRASHED:{Colors.RESET} {e}")
        print(f"{Colors.YELLOW}This is ironic.{Colors.RESET}")
        print(f"{Colors.CYAN}→{Colors.RESET} Please report this at: https://github.com/AymanHaidry/Kosmosic-Orbiton/issues")
        # PAUSE
        print(f"\n  {Colors.DIM}Press Enter to exit...{Colors.RESET}")
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        sys.exit(1)
