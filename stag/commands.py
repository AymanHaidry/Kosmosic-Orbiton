"""Command handlers; kept separate from the input and presentation loops."""
import math
import os
import platform
import random
import re
import subprocess
import shutil
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

try:
    from rich.table import Table
    from rich import box
except ImportError:
    Table = box = None

from .config import CONFIG, PROJECTS, STREETVIEW_LOCATIONS, TOXIC_ROASTS
from .device import DeviceController
from .math_engine import MathNormalizer
from .memory import UserMemory
from .nlp import NaturalLanguageProcessor
from .ui import NeuroInterface
from .voice import VoiceManager

class CommandEngine:
    def __init__(self, ui: NeuroInterface, voice: VoiceManager, memory: UserMemory, intel):
        self.ui = ui
        self.voice = voice
        self.memory = memory
        self.intel = intel
        self.chrome = CONFIG["chrome_path"].get(platform.system(), "chrome")
        self.current_folder = Path.home()
        self.command_history: List[str] = []

    def open_chrome(self, url: str, args: List[str] = None):
        cmd = [self.chrome, url]
        if args:
            cmd.extend(args)
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            webbrowser.open(url)
            return True

    def speak(self, text: str):
        """Always speak feedback naturally."""
        self.voice.speak(text)

    # ─── EXISTING HANDLERS ─────────────────────────────────
    def handle_search(self, query: str):
        url = f"https://www.google.com/search?q={quote(query)}"
        self.open_chrome(url)
        msg = f"Searching Google for {query}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_youtube(self, query: str):
        url = f"https://www.youtube.com/results?search_query={quote(query)}"
        self.open_chrome(url)
        msg = f"Searching YouTube for {query}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_calculate(self, expr: str):
        try:
            normalized = MathNormalizer.normalize(expr)
            result = MathNormalizer.safe_eval(normalized)
            msg = f"The answer is {result}"
            self.ui.show_success(f"Result: {result}")
            self.speak(msg)
        except ValueError as e:
            self.ui.show_error(f"Calculation failed: {e}")
            self.speak("Sorry, I couldn't understand that math problem.")

    def handle_weather(self, city: str = ""):
        if city:
            url = f"https://www.google.com/search?q=weather+{quote(city)}"
            self.open_chrome(url)
            msg = f"Opening weather for {city}"
        else:
            self.open_chrome("https://www.google.com/search?q=weather")
            msg = "Opening local weather"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_airport(self, city: str):
        url = f"https://www.google.com/search?q={quote(city)}+airport"
        self.open_chrome(url)
        msg = f"Searching airport info for {city}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_track(self, flight: str):
        flight_clean = flight.replace(" ", "").upper()
        url = f"https://www.flightradar24.com/{flight_clean}"
        self.open_chrome(url)
        msg = f"Tracking flight {flight_clean} on FlightRadar24"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_metar(self, icao: str):
        icao_clean = icao.upper()[:4]
        url = f"https://www.aviationweather.gov/metar?ids={icao_clean}"
        self.open_chrome(url)
        msg = f"Fetching METAR for {icao_clean}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_open_file(self, target: str):
        target = target.lower().strip()
        home = Path.home()
        folder_map = {
            "downloads": home / "Downloads",
            "documents": home / "Documents",
            "desktop": home / "Desktop",
            "pictures": home / "Pictures",
            "videos": home / "Videos",
            "music": home / "Music",
        }
        if target in folder_map:
            path = folder_map[target]
            if path.exists():
                self.current_folder = path
                self._open_file_explorer(path)
                self.ui.show_success(f"Opened: {target}")
                self.speak(f"Opening {target} folder in File Explorer")
                self.ui.show_file_list(path)
                return
        ext_match = re.search(r"latest\s+(\w+)\s*(?:file)?", target)
        if ext_match:
            ext = ext_match.group(1)
            ext_map = {"pdf": ".pdf", "word": ".docx", "python": ".py",
                      "excel": ".xlsx", "image": ".jpg", "text": ".txt",
                      "powerpoint": ".pptx", "video": ".mp4"}
            search_ext = ext_map.get(ext, f".{ext}")
            found = self.find_latest_file(home, search_ext)
            if found:
                self.open_path(found)
                msg = f"Opened your latest {ext} file: {found.name}"
                self.ui.show_success(msg)
                self.speak(msg)
                return
            else:
                self.ui.show_error(f"No {ext} files found")
                self.speak(f"I could not find any {ext} files.")
                return
        matches = []
        for root, dirs, files in os.walk(home):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["AppData", "node_modules"]]
            for f in files:
                if target in f.lower():
                    matches.append(Path(root) / f)
            if len(matches) > 20:
                break
        if matches:
            best = max(matches, key=lambda p: p.stat().st_mtime)
            self.open_path(best)
            msg = f"Opened {best.name}"
            self.ui.show_success(msg)
            self.speak(msg)
        else:
            self.ui.show_error(f"No files matching '{target}' found")
            self.speak("I could not find any files matching that name.")

    def _open_file_explorer(self, path: Path):
        if sys.platform == "win32":
            subprocess.Popen(["explorer.exe", str(path)])
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])

    def handle_folder_nav(self, target: str):
        target = target.lower().strip()
        if target in ("parent", "back", "up"):
            parent = self.current_folder.parent
            if parent.exists():
                self.current_folder = parent
                self._open_file_explorer(parent)
                msg = f"Navigated up to {parent.name}"
                self.ui.show_success(msg)
                self.speak(msg)
                self.ui.show_file_list(parent)
            return
        potential = self.current_folder / target
        if potential.exists() and potential.is_dir():
            self.current_folder = potential
            self._open_file_explorer(potential)
            msg = f"Entered {target}"
            self.ui.show_success(msg)
            self.speak(msg)
            self.ui.show_file_list(potential)
            return
        potential_home = Path.home() / target
        if potential_home.exists() and potential_home.is_dir():
            self.current_folder = potential_home
            self._open_file_explorer(potential_home)
            msg = f"Jumped to {target}"
            self.ui.show_success(msg)
            self.speak(msg)
            self.ui.show_file_list(potential_home)
            return
        self.ui.show_error(f"Folder not found: {target}")
        self.speak(f"I could not find a folder named {target}.")

    def handle_project(self, name: str):
        path = PROJECTS.get(name.lower())
        if not path or not os.path.exists(path):
            self.ui.show_error(f"Project not found: {name}")
            self.speak(f"I could not find the project {name}.")
            return

        executable = None
        if sys.platform == "win32":
            candidates = [
                Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Microsoft VS Code/Code.exe",
                Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Microsoft VS Code/Code.exe",
                Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Microsoft VS Code/Code.exe",
            ]
            executable = next((str(candidate) for candidate in candidates if candidate.is_file()), None)
            if executable is None:
                candidate = shutil.which("code.exe")
                if candidate and Path(candidate).suffix.lower() == ".exe":
                    executable = candidate
        else:
            executable = shutil.which("code")

        if not executable:
            self.ui.show_error("VS Code was not found. Install it or add its CLI to PATH.")
            self.speak("I could not find Visual Studio Code.")
            return

        try:
            subprocess.Popen(
                [executable, str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
            )
        except OSError as exc:
            self.ui.show_error(f"Could not launch VS Code: {exc}")
            return

        msg = f"Opening project {name} in VS Code"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_run(self, name: str):
        home = Path.home()
        candidates = list(home.rglob("*.py"))
        candidates = [c for c in candidates if name.lower() in c.name.lower()]
        if candidates:
            script = candidates[0]
            subprocess.Popen([sys.executable, str(script)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            msg = f"Running {script.name}"
            self.ui.show_success(msg)
            self.speak(msg)
        else:
            self.ui.show_error(f"Script not found: {name}")
            self.speak(f"I could not find a script named {name}.")

    def handle_clipboard(self, mode: str = "google"):
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            elif platform.system() == "Darwin":
                result = subprocess.run(
                    ["pbpaste"], capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            else:
                result = subprocess.run(
                    ["xclip", "-selection", "clipboard", "-o"],
                    capture_output=True, text=True, timeout=3
                )
                text = result.stdout.strip()
            if not text:
                self.ui.show_error("Clipboard is empty")
                self.speak("Your clipboard is empty.")
                return
            msg = f"Searching clipboard content: {text[:30]}..."
            self.ui.show_success(msg)
            self.speak("Searching your clipboard content.")
            if "youtube" in mode:
                self.handle_youtube(text)
            else:
                self.handle_search(text)
        except Exception as e:
            self.ui.show_error(f"Clipboard error: {e}")
            self.speak("I had trouble reading your clipboard.")

    def handle_motivate(self):
        roast = random.choice(TOXIC_ROASTS)
        self.ui.show_roast(roast)
        self.speak(roast)

    def handle_status(self):
        uptime = datetime.now() - self.ui.session_start
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        if self.ui.console:
            table = Table(title="Status Report", box=box.SIMPLE)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Uptime", f"{hours}h {minutes}m {seconds}s")
            table.add_row("Commands", str(self.ui.total_commands))
            table.add_row("Errors", str(self.ui.error_count))
            table.add_row("Current Dir", str(self.current_folder))
            self.ui.console.print(table)
        else:
            print(f"\n📊 Status Report")
            print(f"   Uptime: {hours}h {minutes}m")
            print(f"   Commands: {self.ui.total_commands}")
            print(f"   Errors: {self.ui.error_count}")
            print(f"   Current: {self.current_folder}\n")
        self.speak(f"Status report. Uptime is {hours} hours and {minutes} minutes. You have issued {self.ui.total_commands} commands with {self.ui.error_count} errors.")

    def handle_exam_mode(self):
        self.open_chrome("https://www.google.com/search?q=calculator")
        time.sleep(0.5)
        self.open_chrome("https://www.desmos.com/scientific")
        time.sleep(0.5)
        if platform.system() == "Windows":
            subprocess.Popen(["notepad.exe"])
        msg = "Exam mode activated. Focus or perish."
        self.ui.show_success("EXAM MODE ACTIVATED. No excuses.")
        self.speak(msg)

    def handle_streetview(self):
        lat, lng, desc = random.choice(STREETVIEW_LOCATIONS)
        url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}"
        self.open_chrome(url)
        msg = f"Transporting you to {desc}"
        self.ui.show_success(f"🌍 Street View: {desc}")
        self.speak(msg)

    def handle_maps(self, place: str):
        url = f"https://www.google.com/maps/search/{quote(place)}"
        self.open_chrome(url)
        msg = f"Showing maps for {place}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_time(self):
        now = datetime.now().strftime("%I:%M %p")
        msg = f"It is {now}"
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_help(self):
        self.ui.show_help()
        self.speak("Here is the full command list. You can say search, youtube, calculate, weather, airport, track flight, metar, open files, navigate folders, open projects, run scripts, maps, street view, clipboard search, motivate me, status report, exam mode, who am I, tell me about, battery, volume, brightness, wifi, bluetooth, system, reboot, help, sleep, or wake.")

    def handle_reboot(self):
        self.speak("Rebooting Orbiton. See you in a moment.")
        self.ui.show_info("🔄 Rebooting...")
        time.sleep(1)
        subprocess.Popen([sys.executable, "-m", "stag"], 
                        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        sys.exit(0)

    def handle_whoami(self):
        info = self.memory.recall()
        self.ui.show_info(f"🧠 {info}")
        self.speak(info)

    def handle_knowledge(self, topic: str):
        result = self.intel.process(f"tell me about {topic}")
        if result[0] == "knowledge" and result[1]:
            self.ui.show_knowledge(topic, result[1])
            self.speak(result[1])
        else:
            self.handle_search(topic)

    def handle_sleep(self):
        self.speak("Going to sleep. Press your headset button twice or say Tokyo to wake me.")
        self.ui.show_info("💤 Manual sleep activated")
        return "sleep"

    def handle_wake(self):
        self.speak("I am awake. What do you need?")
        self.ui.show_success("🌙 Tokyo is awake")
        return "wake"

    # ═════════════════════════════════════════════════════════════
    #  🔧 DEVICE HANDLERS
    # ═════════════════════════════════════════════════════════════

    def handle_battery(self):
        """Check battery level and status"""
        info = DeviceController.get_battery()
        self.ui.show_battery(info)
        if "error" in info:
            self.speak(f"Battery check failed: {info['error']}")
        else:
            pct = info.get("percent", "?")
            status = info.get("status", "Unknown")
            plugged = "plugged in" if info.get("plugged") else "on battery power"
            self.speak(f"Battery is at {pct} percent. Status: {status}. You are {plugged}.")

    def handle_volume(self, args: str = ""):
        """Control system volume: read, set, mute, unmute"""
        args = args.lower().strip()

        # Mute / Unmute
        if "mute" in args and "un" not in args:
            result = DeviceController.mute(True)
            if result.get("success"):
                self.ui.show_volume({"percent": 0, "muted": True})
                self.speak("Muted.")
            else:
                self.ui.show_error(f"Mute failed: {result.get('error')}")
                self.speak(f"Could not mute: {result.get('error')}")
            return

        if "unmute" in args:
            result = DeviceController.mute(False)
            if result.get("success"):
                info = DeviceController.get_volume()
                self.ui.show_volume(info)
                self.speak("Unmuted.")
            else:
                self.ui.show_error(f"Unmute failed: {result.get('error')}")
                self.speak(f"Could not unmute: {result.get('error')}")
            return

        # Set volume
        level = NaturalLanguageProcessor.extract_volume_level(args)
        if level is not None:
            result = DeviceController.set_volume(level)
            if result.get("success"):
                self.ui.show_volume({"percent": level, "muted": False})
                self.speak(f"Volume set to {level} percent.")
            else:
                self.ui.show_error(f"Volume failed: {result.get('error')}")
                self.speak(f"Could not set volume: {result.get('error')}")
            return

        # Read volume
        info = DeviceController.get_volume()
        self.ui.show_volume(info)
        if "error" in info:
            self.speak(f"Volume check failed: {info['error']}")
        else:
            pct = info.get("percent", "?")
            muted = "muted" if info.get("muted") else "unmuted"
            self.speak(f"Volume is at {pct} percent. Currently {muted}.")

    def handle_brightness(self, args: str = ""):
        """Control screen brightness: read or set"""
        args = args.lower().strip()

        level = NaturalLanguageProcessor.extract_brightness_level(args)
        if level is not None:
            result = DeviceController.set_brightness(level)
            if result.get("success"):
                self.ui.show_brightness({"percent": level})
                self.speak(f"Brightness set to {level} percent.")
            else:
                self.ui.show_error(f"Brightness failed: {result.get('error')}")
                self.speak(f"Could not set brightness: {result.get('error')}")
            return

        info = DeviceController.get_brightness()
        self.ui.show_brightness(info)
        if "error" in info:
            self.speak(f"Brightness check failed: {info['error']}")
        else:
            self.speak(f"Brightness is at {info.get('percent', '?')} percent.")

    def handle_wifi(self, args: str = ""):
        """WiFi: list networks, connect with numbered selection + dialog"""
        args = args.lower().strip()

        if "list" in args or "scan" in args or "show" in args or not args:
            networks = DeviceController.get_wifi_networks()
            self.ui.show_wifi_list(networks)

            if not networks or (len(networks) == 1 and "error" in networks[0]):
                err = networks[0].get("error", "Unknown") if networks else "No networks"
                self.speak(f"WiFi scan failed: {err}")
                return

            self.speak(f"Found {len(networks)} networks. Check the list and say 'connect to wifi' to pick one.")
            return

        if "connect" in args:
            networks = DeviceController.get_wifi_networks()
            if not networks or (len(networks) == 1 and "error" in networks[0]):
                err = networks[0].get("error", "Unknown") if networks else "No networks"
                self.speak(f"WiFi scan failed: {err}")
                return

            self.ui.show_wifi_list(networks)
            self.speak(f"Pick a network by number, 1 through {min(len(networks), 15)}.")

            # Prompt for selection
            if self.ui.console:
                self.ui.console.print("[cyan]Enter number to connect, or 'cancel':[/cyan]")
            else:
                print("\nEnter number to connect, or 'cancel':")

            try:
                choice = input("> ").strip()
                if choice.lower() == 'cancel':
                    self.speak("Cancelled.")
                    return

                idx = int(choice) - 1
                if idx < 0 or idx >= len(networks):
                    self.ui.show_error("Invalid selection.")
                    self.speak("That number is not on the list.")
                    return

                selected = networks[idx]
                ssid = selected.get("ssid", "")
                if not ssid or ssid == "Hidden":
                    self.ui.show_error("Cannot connect to hidden network this way.")
                    self.speak("Cannot connect to a hidden network.")
                    return

                # Try connecting without password first
                result = DeviceController.connect_wifi(ssid)

                if result.get("needs_password"):
                    # Dialog for password
                    try:
                        import tkinter as tk
                        from tkinter import simpledialog
                        root = tk.Tk()
                        root.withdraw()
                        root.geometry("+500+300")
                        password = simpledialog.askstring(
                            "WiFi Password",
                            f"Enter password for '{ssid}':",
                            show='*'
                        )
                        root.destroy()
                    except Exception:
                        # Fallback to terminal input
                        password = input(f"Password for '{ssid}': ").strip()

                    if password:
                        result = DeviceController.connect_wifi(ssid, password)
                    else:
                        self.speak("No password provided. Cancelled.")
                        return

                if result.get("success"):
                    self.ui.show_success(f"Connected to {ssid}")
                    self.speak(f"Connected to {ssid}.")
                else:
                    self.ui.show_error(f"Connection failed: {result.get('error')}")
                    self.speak(f"Could not connect: {result.get('error')}")

            except ValueError:
                self.ui.show_error("Invalid input.")
                self.speak("Please enter a number.")
            except Exception as e:
                self.ui.show_error(f"WiFi error: {e}")
                self.speak(f"WiFi connection error: {e}")
            return

        # Default: show networks
        self.handle_wifi("list")

    def handle_bluetooth(self, args: str = ""):
        """Bluetooth: list devices, toggle on/off"""
        args = args.lower().strip()

        if "on" in args:
            result = DeviceController.toggle_bluetooth(True)
            if result.get("success"):
                self.ui.show_success("Bluetooth enabled")
                self.speak("Bluetooth is now on.")
            else:
                self.ui.show_error(f"Bluetooth error: {result.get('error')}")
                self.speak(f"Could not enable Bluetooth: {result.get('error')}")
            return

        if "off" in args:
            result = DeviceController.toggle_bluetooth(False)
            if result.get("success"):
                self.ui.show_success("Bluetooth disabled")
                self.speak("Bluetooth is now off.")
            else:
                self.ui.show_error(f"Bluetooth error: {result.get('error')}")
                self.speak(f"Could not disable Bluetooth: {result.get('error')}")
            return

        if "list" in args or "devices" in args or not args:
            devices = DeviceController.get_bluetooth_devices()
            self.ui.show_bluetooth_devices(devices)
            if not devices or (len(devices) == 1 and "error" in devices[0]):
                err = devices[0].get("error", "Unknown") if devices else "None found"
                self.speak(f"Bluetooth scan failed: {err}")
            else:
                self.speak(f"Found {len(devices)} Bluetooth devices.")
            return

        # Default
        self.handle_bluetooth("list")

    def handle_system(self):
        """Show system info: CPU, RAM, disk"""
        info = DeviceController.get_system_info()
        self.ui.show_system_info(info)
        if "error" in info:
            self.speak(f"System info failed: {info['error']}")
        else:
            plat = info.get("platform", "Unknown")
            cpu = info.get("cpu_percent", "?")
            mem_pct = info.get("memory_percent", "?")
            disk_free = info.get("disk_free_gb", "?")
            self.speak(f"System status. Platform: {plat}. CPU usage: {cpu} percent. Memory usage: {mem_pct} percent. Disk free: {disk_free} gigabytes.")

    def open_path(self, path: Path):
        if platform.system() == "Windows":
            os.startfile(str(path))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])

    def find_latest_file(self, root: Path, ext: str) -> Optional[Path]:
        files = []
        for p in root.rglob(f"*{ext}"):
            if p.is_file() and not any(x in str(p) for x in ["AppData", "node_modules", ".git"]):
                files.append(p)
        if not files:
            return None
        return max(files, key=lambda p: p.stat().st_mtime)


