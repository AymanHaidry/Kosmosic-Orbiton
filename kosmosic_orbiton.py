#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎧 Orbiton v0.8.0 — Voice Command Terminal
  "We put the world around your head."
  Wake word: TOKYO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import speech_recognition as sr
import webbrowser
import subprocess
import sys
import os
import re
import json
import time
import random
import math
import platform
import threading
import queue
import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from typing import Optional, Dict, List, Tuple

# ─── OPTIONAL IMPORTS ──────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# ─── INTELLIGENCE MODULE ───────────────────────────────────
from neuro_link_intel import get_intelligence, NaturalLanguageProcessor, MathNormalizer

# ─── CONFIGURATION ───────────────────────────────────────────
CONFIG = {
    "chrome_path": {
        "Windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
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
    "post_tts_silence": 0.5,
}

# Toxic motivation database
TOXIC_ROASTS = [
    "The Doha apartment is not paying for itself. Get back to work, peasant.",
    "Your GitHub contribution graph looks like a deforestation map. Embarrassing.",
    "That idea you had 3 hours ago? Someone in Bangalore already shipped it.",
    "Your sleep schedule is a war crime. Fix yourself.",
    "You opened this assistant to avoid work. I see you. I judge you.",
    "Your code has more bugs than a Mumbai street food stall. Write a test.",
    "That quick break was 47 minutes ago. You disgust me.",
    "Your ancestors built empires. You can not even close 3 Chrome tabs.",
    "I ran a diagnostic on your life. Critical failure across all sectors.",
    "You have the focus of a goldfish on TikTok. Pathetic.",
    "Your last commit message was fix stuff. You are a disappointment.",
    "While you were procrastinating, your competitor learned Rust. You are done.",
    "Your to-do list is older than some civilizations. Start item one.",
    "I calculated your productivity. The result made my circuits cry.",
    "You call this grinding? I have seen sloths with more hustle.",
    # ─── DEVICE ROASTS ───
    "Your battery is lower than your standards. Charge it.",
    "You are asking me to check your volume because you are too lazy to look at the tray icon. Pathetic.",
    "Your screen brightness is the only thing dimmer than your career prospects.",
    "You have 47 WiFi networks available and you still cannot connect to productivity.",
    "Your Bluetooth is off. Much like your social life.",
]

# Random Street View locations (amazing places)
STREETVIEW_LOCATIONS = [
    (35.0116, 135.7681, "Kyoto, Japan — Arashiyama Bamboo Grove"),
    (64.1466, -21.9426, "Reykjavik, Iceland — Northern Lights Spot"),
    (48.8584, 2.2945, "Paris, France — Eiffel Tower"),
    (-33.8568, 151.2153, "Sydney, Australia — Opera House"),
    (37.8199, -122.4783, "San Francisco, USA — Golden Gate Bridge"),
    (25.1972, 55.2744, "Dubai, UAE — Burj Khalifa"),
    (51.1788, -1.8262, "Stonehenge, UK"),
    (27.1751, 78.0421, "Agra, India — Taj Mahal"),
    (43.6426, -79.3871, "Toronto, Canada — CN Tower"),
    (55.7558, 37.6173, "Moscow, Russia — Red Square"),
    (40.4319, 116.5704, "Great Wall of China"),
    (-13.1631, -72.5450, "Machu Picchu, Peru"),
    (41.9028, 12.4964, "Rome, Italy — Colosseum"),
    (59.3293, 18.0686, "Stockholm, Sweden — Gamla Stan"),
    (1.3521, 103.8198, "Singapore — Marina Bay Sands"),
    (45.4215, -75.6972, "Ottawa, Canada — Parliament"),
    (35.6762, 139.6503, "Tokyo, Japan — Shibuya Crossing"),
    (48.1351, 11.5820, "Munich, Germany — Marienplatz"),
    (52.5200, 13.4050, "Berlin, Germany — Brandenburg Gate"),
    (47.4979, 19.0402, "Budapest, Hungary — Parliament"),
]

# Project shortcuts
PROJECTS: Dict[str, str] = {
    "hex link": r"C:\Projects\hex-link",
    "runway objects": r"C:\Projects\runway-objects",
    "udestini": r"C:\Projects\udestini",
}

# Kosmosic URLs
KOSMOSIC_URL = "https://kosmosic.vercel.app"
KOSMOSIC_APP = "https://kosmosic.vercel.app/app"

# Master command list for help display
ALL_COMMANDS = [
    ("🎓 Study", "kosmosic", "Open Kosmosic study dashboard"),
    ("🔍 Search", "search <query>", "Google search anything"),
    ("🎥 YouTube", "youtube <query>", "Search YouTube"),
    ("🧮 Math", "calculate <expr>", "Calculate and speak result"),
    ("🌤 Weather", "weather [city]", "Check weather"),
    ("✈️ Airport", "airport <city>", "Search airport info"),
    ("🛫 Track", "track <flight>", "Track flight on FlightRadar"),
    ("📡 METAR", "metar <icao>", "Aviation weather report"),
    ("📂 Files", "open <name/folder>", "Open files or folders"),
    ("📁 Navigate", "go to <folder>", "Navigate filesystem"),
    ("💻 Projects", "open project <name>", "Open VS Code project"),
    ("🐍 Run", "run <script>", "Run Python script"),
    ("🗺 Maps", "maps <place>", "Google Maps search"),
    ("🌍 StreetView", "streetview", "Random amazing place"),
    ("📋 Clipboard", "clipboard [google/youtube]", "Search clipboard"),
    ("💀 Motivate", "motivate me", "Toxic motivation roast"),
    ("📊 Status", "status report", "Session statistics"),
    ("🚀 Exam Mode", "exam mode", "Launch study tools"),
    ("🕐 Time", "what time is it", "Current time"),
    ("🧠 Memory", "who am i", "Recall stored user info"),
    ("🧠 Intel", "tell me about <topic>", "Knowledge lookup"),
    # ─── DEVICE COMMANDS ───
    ("🔋 Battery", "battery", "Check battery level & status"),
    ("🔊 Volume", "volume [set/mute/unmute]", "Control system volume"),
    ("💡 Brightness", "brightness [set <0-100>]", "Control screen brightness"),
    ("📶 WiFi", "wifi [list/connect]", "Scan & connect to networks"),
    ("🔷 Bluetooth", "bluetooth [list/on/off]", "Manage Bluetooth devices"),
    ("🖥 System", "system", "CPU, RAM, disk & platform info"),
    ("🔄 Reboot", "reboot", "Restart Orbiton"),
    ("❓ Help", "help", "Show this command list"),
    ("😴 Sleep", "sleep", "Put Tokyo to sleep"),
    ("🌙 Wake", "wake / Tokyo", "Wake Tokyo up"),
]


class NeuroInterface:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.headphone_name: Optional[str] = None
        self.error_count = 0
        self.total_commands = 0
        self.session_start = datetime.now()

    def clear(self):
        os.system("cls" if sys.platform == "win32" else "clear")

    def show_boot_sequence(self):
        """Apple-style minimalist boot sequence"""
        if self.console:
            self.console.print(Panel(
                "[bold white]●[/bold white]",
                border_style="white",
                box=box.ROUNDED,
                width=10
            ))
            time.sleep(0.5)
            self.console.print("[dim]Loading Orbiton...[/dim]")
            time.sleep(0.5)
            self.console.print("[dim]Waking up Tokyo...[/dim]")
            time.sleep(0.5)
            self.console.print("[dim]Initializing voice engine...[/dim]")
            time.sleep(0.5)
            self.console.print("[dim]Connecting to intelligence module...[/dim]")
            time.sleep(0.5)
            self.console.print("[green]✓ Ready[/green]")
            time.sleep(0.3)
        else:
            print("\n   ●")
            time.sleep(0.5)
            print("   Loading Orbiton...")
            time.sleep(0.5)
            print("   Waking up Tokyo...")
            time.sleep(0.5)
            print("   Initializing voice engine...")
            time.sleep(0.5)
            print("   Connecting to intelligence...")
            time.sleep(0.5)
            print("   ✓ Ready")
            time.sleep(0.3)

    def show_banner(self):
        if self.console:
            banner = Panel.fit(
                Text.from_markup(
                    "[bold cyan]🎧 Kosmosic Orbiton v0.8.0[/bold cyan]\n"
                    "[dim]Voice Command Terminal — Say TOKYO to wake[/dim]\n"
                    f"[green]Headset:[/green] {self.headphone_name or 'Scanning...'}\n"
                    f"[yellow]Session:[/yellow] {self.session_start.strftime('%H:%M:%S')}"
                ),
                border_style="cyan",
                box=box.DOUBLE
            )
            self.console.print(banner)
        else:
            print("=" * 50)
            print("🎧 Kosmosic Orbiton v0.8.0 — Say TOKYO to wake")
            print(f"Headset: {self.headphone_name or 'Scanning...'}")
            print("=" * 50)

    def show_listening(self, active: bool = True):
        if self.console:
            if active:
                self.console.print(Panel(
                    "[bold magenta]🎤 LISTENING...[/bold magenta]",
                    border_style="magenta",
                    width=40
                ))
            else:
                self.console.print(Panel(
                    "[dim]💤 SLEEPING... Press button or say TOKYO to wake[/dim]",
                    border_style="dim",
                    width=50
                ))
        else:
            if active:
                print("\n╔══════════════════════════════════════╗")
                print("║         🎤  LISTENING...             ║")
                print("╚══════════════════════════════════════╝")
            else:
                print("\n╔══════════════════════════════════════╗")
                print("║         💤  SLEEPING...              ║")
                print("╚══════════════════════════════════════╝")

    def show_heard(self, text: str):
        if self.console:
            self.console.print(f"[dim]🎯 Heard:[/dim] [italic]\"{text}\"[/italic]")
        else:
            print(f'🎯 Heard: \"{text}\"')

    def show_success(self, msg: str):
        if self.console:
            self.console.print(f"[bold green]✅ {msg}[/bold green]")
        else:
            print(f"✅ {msg}")

    def show_error(self, msg: str):
        self.error_count += 1
        if self.console:
            self.console.print(f"[bold red]❌ {msg}[/bold red]")
        else:
            print(f"❌ {msg}")

    def show_info(self, msg: str):
        if self.console:
            self.console.print(f"[cyan]ℹ️  {msg}[/cyan]")
        else:
            print(f"ℹ️  {msg}")

    def show_roast(self, roast: str):
        if self.console:
            self.console.print(Panel(
                f"[bold red]💀 {roast}[/bold red]",
                title="[yellow]TOXIC MOTIVATION[/yellow]",
                border_style="red",
                box=box.HEAVY
            ))
        else:
            print(f"\n💀 TOXIC MOTIVATION: {roast}\n")

    def show_command_table(self):
        if not self.console:
            print("\nCommands: search, youtube, calculate, weather, airport, track, metar, open, run, motivate, streetview, maps, clipboard, status, exam mode, kosmosic, help, reboot, who am i, sleep, wake, tell me about")
            print("Device: battery, volume, brightness, wifi, bluetooth, system")
            return
        table = Table(title="Available Commands", box=box.SIMPLE_HEAD)
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Command", style="green")
        table.add_column("Example", style="dim")
        for cat, cmd, ex in ALL_COMMANDS:
            table.add_row(cat, cmd, ex)
        self.console.print(table)

    def show_help(self):
        """Display all commands in a beautiful panel"""
        if self.console:
            help_text = "\n".join([f"[green]{cmd}[/green] — [dim]{desc}[/dim]" for _, cmd, desc in ALL_COMMANDS])
            self.console.print(Panel(
                help_text,
                title="[bold cyan]📖 ORBITON COMMAND MANUAL[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED
            ))
        else:
            print("\n📖 ORBITON COMMAND MANUAL")
            for cat, cmd, desc in ALL_COMMANDS:
                print(f"   {cmd:25} — {desc}")
            print()

    def show_file_list(self, folder: Path):
        """Show files in a folder as a numbered list"""
        if self.console:
            try:
                items = sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
                table = Table(title=f"📂 {folder.name}", box=box.SIMPLE)
                table.add_column("#", style="dim", width=4)
                table.add_column("Type", style="cyan", width=6)
                table.add_column("Name", style="green")
                for i, item in enumerate(items[:30], 1):
                    icon = "📁" if item.is_dir() else "📄"
                    table.add_row(str(i), icon, item.name)
                self.console.print(table)
            except Exception as e:
                self.show_error(f"Cannot list folder: {e}")
        else:
            try:
                items = sorted(folder.iterdir(), key=lambda p: p.name.lower())
                print(f"\n📂 {folder.name}")
                for i, item in enumerate(items[:30], 1):
                    icon = "[DIR]" if item.is_dir() else "[FILE]"
                    print(f"   {i:2}. {icon} {item.name}")
                print()
            except Exception as e:
                self.show_error(f"Cannot list folder: {e}")

    def show_knowledge(self, topic: str, fact: str):
        """Display knowledge lookup result"""
        if self.console:
            self.console.print(Panel(
                f"[green]{fact}[/green]",
                title=f"[bold cyan]🧠 {topic.title()}[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED
            ))
        else:
            print(f"\n🧠 {topic.title()}: {fact}\n")

    # ─── DEVICE DISPLAY METHODS ───
    def show_battery(self, info: Dict):
        """Beautiful battery display"""
        if "error" in info:
            self.show_error(f"Battery: {info['error']}")
            return
        pct = info.get("percent", "?")
        status = info.get("status", "Unknown")
        plugged = info.get("plugged", False)

        if self.console:
            icon = "🔌" if plugged else "🔋"
            color = "green" if (pct != "?" and int(pct) > 50) else "yellow" if (pct != "?" and int(pct) > 20) else "red"
            self.console.print(Panel(
                f"[{color}]{icon} {pct}%[/{color}]\n[dim]Status: {status}[/dim]\n[dim]{'Plugged in' if plugged else 'On battery'}[/dim]",
                title="[bold cyan]🔋 BATTERY[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED
            ))
        else:
            icon = "🔌" if plugged else "🔋"
            print(f"\n{icon} Battery: {pct}% | Status: {status} | {'Plugged in' if plugged else 'On battery'}\n")

    def show_volume(self, info: Dict):
        """Beautiful volume display"""
        if "error" in info:
            self.show_error(f"Volume: {info['error']}")
            return
        pct = info.get("percent", "?")
        muted = info.get("muted", False)

        if self.console:
            if muted:
                bar = "🔇 MUTED"
                color = "red"
            else:
                level = int(pct) if pct != "?" else 0
                filled = "█" * (level // 10)
                empty = "░" * (10 - level // 10)
                bar = f"{filled}{empty} {pct}%"
                color = "green" if level > 50 else "yellow" if level > 20 else "red"
            self.console.print(Panel(
                f"[{color}]{bar}[/{color}]",
                title="[bold cyan]🔊 VOLUME[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED
            ))
        else:
            state = "MUTED" if muted else f"{pct}%"
            print(f"\n🔊 Volume: {state}\n")

    def show_brightness(self, info: Dict):
        """Beautiful brightness display"""
        if "error" in info:
            self.show_error(f"Brightness: {info['error']}")
            return
        pct = info.get("percent", "?")

        if self.console:
            level = int(pct) if pct != "?" else 0
            filled = "█" * (level // 10)
            empty = "░" * (10 - level // 10)
            bar = f"{filled}{empty} {pct}%"
            color = "yellow" if level > 50 else "dim"
            self.console.print(Panel(
                f"[{color}]{bar}[/{color}]",
                title="[bold cyan]💡 BRIGHTNESS[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED
            ))
        else:
            print(f"\n💡 Brightness: {pct}%\n")

    def show_wifi_list(self, networks: List[Dict]):
        """Beautiful WiFi network list"""
        if not networks or (len(networks) == 1 and "error" in networks[0]):
            err = networks[0].get("error", "Unknown error") if networks else "No networks found"
            self.show_error(f"WiFi: {err}")
            return

        if self.console:
            table = Table(title="📶 Available WiFi Networks", box=box.SIMPLE_HEAD)
            table.add_column("#", style="dim", width=4, justify="right")
            table.add_column("SSID", style="green")
            table.add_column("Signal", style="cyan")
            table.add_column("Security", style="yellow")
            for i, net in enumerate(networks[:15], 1):
                ssid = net.get("ssid", "Hidden")
                sig = net.get("signal", "?")
                sec = net.get("security", "?")
                table.add_row(str(i), ssid, sig, sec)
            self.console.print(table)
        else:
            print("\n📶 Available WiFi Networks")
            for i, net in enumerate(networks[:15], 1):
                ssid = net.get("ssid", "Hidden")
                sig = net.get("signal", "?")
                sec = net.get("security", "?")
                print(f"   {i:2}. {ssid:25} | {sig:10} | {sec}")
            print()

    def show_bluetooth_devices(self, devices: List[Dict]):
        """Beautiful Bluetooth device list"""
        if not devices or (len(devices) == 1 and "error" in devices[0]):
            err = devices[0].get("error", "Unknown error") if devices else "No devices found"
            self.show_error(f"Bluetooth: {err}")
            return

        if self.console:
            table = Table(title="🔷 Bluetooth Devices", box=box.SIMPLE_HEAD)
            table.add_column("#", style="dim", width=4)
            table.add_column("Name", style="green")
            table.add_column("Status", style="cyan")
            for i, dev in enumerate(devices[:15], 1):
                name = dev.get("name", "Unknown")
                status = dev.get("status", "?")
                table.add_row(str(i), name, status)
            self.console.print(table)
        else:
            print("\n🔷 Bluetooth Devices")
            for i, dev in enumerate(devices[:15], 1):
                name = dev.get("name", "Unknown")
                status = dev.get("status", "?")
                print(f"   {i:2}. {name} | {status}")
            print()

    def show_system_info(self, info: Dict):
        """Beautiful system info display"""
        if "error" in info:
            self.show_error(f"System: {info['error']}")
            return

        if self.console:
            table = Table(title="🖥 System Information", box=box.SIMPLE_HEAD)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Platform", str(info.get("platform", "?")))
            table.add_row("CPU Usage", f"{info.get('cpu_percent', '?')}%")
            table.add_row("Memory", f"{info.get('memory_used_gb', '?')} / {info.get('memory_total_gb', '?')} GB ({info.get('memory_percent', '?')}%)")
            table.add_row("Disk Free", f"{info.get('disk_free_gb', '?')} GB / {info.get('disk_total_gb', '?')} GB")
            self.console.print(table)
        else:
            print("\n🖥 System Information")
            print(f"   Platform: {info.get('platform', '?')}")
            print(f"   CPU: {info.get('cpu_percent', '?')}%")
            print(f"   RAM: {info.get('memory_used_gb', '?')}/{info.get('memory_total_gb', '?')} GB")
            print(f"   Disk: {info.get('disk_free_gb', '?')} GB free")
            print()


class UserMemory:
    """Stores user facts from statements like I am..., I like..., etc."""
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.facts: Dict[str, str] = {}
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.facts = json.load(f)
            except Exception:
                self.facts = {}

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.facts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Memory save error] {e}")

    def learn(self, text: str) -> bool:
        """Extract I am / I like / My ... statements and store them."""
        text = text.lower().strip()
        patterns = [
            (r"(?:i am|i'm|my name is|call me)\s+(.+)", "name"),
            (r"(?:i like|i love|i enjoy)\s+(.+)", "likes"),
            (r"(?:i hate|i dislike)\s+(.+)", "dislikes"),
            (r"(?:i work as|i am a|my job is)\s+(.+)", "job"),
            (r"(?:i live in|i am from|my city is)\s+(.+)", "location"),
            (r"(?:my birthday is|i was born on)\s+(.+)", "birthday"),
            (r"(?:i study|my major is|i am studying)\s+(.+)", "study"),
            (r"(?:my goal is|i want to)\s+(.+)", "goals"),
        ]
        learned = False
        for pattern, key in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip().rstrip(".")
                if key in self.facts:
                    self.facts[key] += f", {value}"
                else:
                    self.facts[key] = value
                learned = True
        if learned:
            self.save()
        return learned

    def recall(self) -> str:
        if not self.facts:
            return "I do not know anything about you yet. Tell me something."
        parts = [f"Your {k} is {v}." for k, v in self.facts.items()]
        return " ".join(parts)

    def recall_one(self, key: str) -> Optional[str]:
        return self.facts.get(key.lower())


class VoiceManager:
    """Natural text-to-speech using edge-tts or system fallback."""
    def __init__(self, voice: str = "en-US-AriaNeural"):
        self.voice = voice
        self.tts_queue = queue.Queue()
        self.tts_active = threading.Event()
        self.post_tts_until = 0.0
        self.post_tts_silence = 1.5
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._tts_worker, daemon=True)
        self._thread.start()

    def _tts_worker(self):
        """Background thread for TTS to avoid blocking."""
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            self.tts_active.set()
            try:
                self._speak_now(text)
            finally:
                self.tts_active.clear()
                with self._lock:
                    self.post_tts_until = time.time() + self.post_tts_silence
            self.tts_queue.task_done()

    def is_listening_blocked(self) -> bool:
        """Return True if mic should stay off (TTS playing or cooling down)."""
        if self.tts_active.is_set():
            return True
        with self._lock:
            return time.time() < self.post_tts_until

    def _speak_now(self, text: str):
        """Actually speak the text."""
        if EDGE_TTS_AVAILABLE:
            try:
                import tempfile
                mp3_path = os.path.join(tempfile.gettempdir(), "neuro_link_tts.mp3")
                asyncio.run(self._edge_speak(text, mp3_path))
                if sys.platform == "win32":
                    try:
                        import pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load(mp3_path)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.05)
                    except ImportError:
                        os.startfile(mp3_path)
                        time.sleep(2)
                elif sys.platform == "darwin":
                    subprocess.run(["afplay", mp3_path], capture_output=True)
                else:
                    subprocess.run(["mpg123", mp3_path], capture_output=True)
                time.sleep(0.5)
                return
            except Exception:
                pass
        self._system_speak(text)

    async def _edge_speak(self, text: str, path: str):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(path)

    def _system_speak(self, text: str):
        if platform.system() == "Windows":
            safe = text.replace("'", "'`'").replace('"', '`"`')
            subprocess.run(
                ["powershell", "-c",
                 f'Add-Type -AssemblyName System.Speech; '
                 f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{safe}")'],
                capture_output=True
            )
        elif platform.system() == "Darwin":
            subprocess.run(["say", text], capture_output=True)
        else:
            subprocess.run(["spd-say", text], capture_output=True)

    def speak(self, text: str):
        """Queue text to be spoken. Always speaks."""
        self.tts_queue.put(text)

    def stop(self):
        self.tts_queue.put(None)


def get_connected_headphones() -> Optional[str]:
    """Detect connected Bluetooth audio device. Best effort per OS."""
    system = platform.system()

    if system == "Windows":
        try:
            ps_cmd = (
                'Get-PnpDevice -Class Bluetooth | '
                'Where-Object {$_.FriendlyName -like "*JBL*" -or '
                '$_.FriendlyName -like "*Headphone*" -or '
                '$_.FriendlyName -like "*Earbud*" -or '
                '$_.FriendlyName -like "*AirPods*" -or '
                '$_.FriendlyName -like "*Sony*" -or '
                '$_.FriendlyName -like "*Bose*"} | '
                'Select-Object -First 1 FriendlyName | '
                'ForEach-Object { $_.FriendlyName }'
            )
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=5
            )
            name = result.stdout.strip()
            if name:
                return name

            ps_cmd2 = (
                'Get-WmiObject Win32_SoundDevice | '
                'Where-Object {$_.Name -like "*Bluetooth*" -or '
                '$_.Name -like "*JBL*"} | '
                'Select-Object -First 1 Name | '
                'ForEach-Object { $_.Name }'
            )
            result2 = subprocess.run(
                ["powershell", "-Command", ps_cmd2],
                capture_output=True, text=True, timeout=5
            )
            name2 = result2.stdout.strip()
            if name2:
                return name2
        except Exception:
            pass

    elif system == "Darwin":
        try:
            result = subprocess.run(
                ["system_profiler", "SPBluetoothDataType", "-json"],
                capture_output=True, text=True, timeout=5
            )
            data = json.loads(result.stdout)
            for item in data.get("SPBluetoothDataType", []):
                for key, val in item.items():
                    if isinstance(val, dict) and val.get("device_connected") == "Yes":
                        if any(x in key.lower() for x in ["jbl", "headphone", "earbud", "airpods", "sony", "bose"]):
                            return key
        except Exception:
            pass

    elif system == "Linux":
        try:
            result = subprocess.run(
                ["bluetoothctl", "info"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.split("\n")
            for line in lines:
                if "Name:" in line:
                    name = line.split("Name:")[1].strip()
                    if any(x in name.lower() for x in ["jbl", "headphone", "earbud", "airpods", "sony", "bose"]):
                        return name
        except Exception:
            pass

    return None


# ═════════════════════════════════════════════════════════════
#  🔧 DEVICE CONTROLLER — Cross-Platform Hardware Control
# ═════════════════════════════════════════════════════════════

class DeviceController:
    """Cross-platform device hardware control. Windows primary, Linux secondary."""

    SYSTEM = platform.system()

    # ── Helper: Run PowerShell safely ───────────────────────
    @classmethod
    def _ps(cls, script: str, timeout: int = 10) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True, text=True, timeout=timeout
        )

    @classmethod
    def _run(cls, cmd: List[str], timeout: int = 10, check: bool = False) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=check)

    # ── Battery ─────────────────────────────────────────────
    @classmethod
    def get_battery(cls) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                ps = ('Get-WmiObject Win32_Battery | '
                      'Select-Object EstimatedChargeRemaining,BatteryStatus | '
                      'ConvertTo-Json')
                result = cls._ps(ps, timeout=5)
                if not result.stdout.strip():
                    return {"error": "No battery detected (desktop PC?)"}
                data = json.loads(result.stdout)
                if isinstance(data, list):
                    data = data[0]
                pct = data.get("EstimatedChargeRemaining", "Unknown")
                status = data.get("BatteryStatus", 0)
                status_map = {1: "Discharging", 2: "Charging", 3: "Fully Charged",
                              4: "Low", 5: "Critical", 6: "Charging", 7: "Charging",
                              8: "Charging", 9: "Charging", 10: "Charging",
                              11: "Partially Charged"}
                return {
                    "percent": pct,
                    "status": status_map.get(status, "Unknown"),
                    "plugged": status in (2, 3, 6, 7, 8, 9, 10, 11)
                }
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                for bat_name in ["BAT0", "BAT1", "BAT2"]:
                    bat_path = Path(f"/sys/class/power_supply/{bat_name}")
                    if bat_path.exists():
                        with open(bat_path / "capacity") as f:
                            pct = int(f.read().strip())
                        with open(bat_path / "status") as f:
                            status = f.read().strip()
                        return {
                            "percent": pct,
                            "status": status,
                            "plugged": status in ("Charging", "Full", "Not charging")
                        }
                return {"error": "No battery found"}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Battery info not supported on {cls.SYSTEM}"}

    # ── Volume ──────────────────────────────────────────────
    @classmethod
    def get_volume(cls) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                nircmd = shutil.which("nircmd.exe")
                if nircmd:
                    result = cls._run([nircmd, "getsysvolume"])
                    if result.returncode == 0:
                        raw = int(result.stdout.strip())
                        pct = round(raw / 655.35, 1)
                        return {"percent": pct, "muted": pct == 0}
                return {"percent": "Unknown", "muted": False,
                        "note": "Install nircmd.exe for precise volume control"}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                result = cls._run(["amixer", "get", "Master"])
                if result.returncode == 0:
                    match = re.search(r'\[(\d+)%\]', result.stdout)
                    muted = "[off]" in result.stdout.lower() or "muted" in result.stdout.lower()
                    return {"percent": int(match.group(1)) if match else 0, "muted": muted}
                result = cls._run(["pactl", "list", "sinks"])
                match = re.search(r'Volume:.*?/(\d+)%', result.stdout)
                muted = "Mute: yes" in result.stdout
                return {"percent": int(match.group(1)) if match else 0, "muted": muted}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Volume not supported on {cls.SYSTEM}"}

    @classmethod
    def set_volume(cls, level: int) -> Dict:
        level = max(0, min(100, level))
        if cls.SYSTEM == "Windows":
            try:
                nircmd = shutil.which("nircmd.exe")
                if nircmd:
                    raw_vol = int(level * 655.35)
                    result = cls._run([nircmd, "setsysvolume", str(raw_vol)])
                    if result.returncode == 0:
                        return {"success": True, "level": level}
                ps = (f'$wsh = New-Object -ComObject WScript.Shell; '
                      f'1..50 | ForEach-Object {{ $wsh.SendKeys([char]174) }}; '
                      f'1..{int(level / 2)} | ForEach-Object {{ $wsh.SendKeys([char]175) }}')
                cls._ps(ps, timeout=5)
                return {"success": True, "level": level, "method": "fallback"}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                cls._run(["amixer", "set", "Master", f"{level}%"], check=True)
                return {"success": True, "level": level}
            except:
                try:
                    cls._run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])
                    return {"success": True, "level": level}
                except Exception as e:
                    return {"error": str(e)}
        return {"error": f"Set volume not supported on {cls.SYSTEM}"}

    @classmethod
    def mute(cls, muted: bool = True) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                nircmd = shutil.which("nircmd.exe")
                if nircmd:
                    flag = "1" if muted else "0"
                    cls._run([nircmd, "mutesysvolume", flag])
                    return {"success": True, "muted": muted}
                cls._ps('$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)')
                return {"success": True, "muted": muted, "method": "fallback"}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                state = "mute" if muted else "unmute"
                cls._run(["amixer", "set", "Master", state], check=True)
                return {"success": True, "muted": muted}
            except:
                try:
                    flag = "1" if muted else "0"
                    cls._run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", flag])
                    return {"success": True, "muted": muted}
                except Exception as e:
                    return {"error": str(e)}
        return {"error": f"Mute not supported on {cls.SYSTEM}"}

    # ── Brightness ──────────────────────────────────────────
    @classmethod
    def get_brightness(cls) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                ps = ('Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness | '
                      'Select-Object CurrentBrightness | ConvertTo-Json')
                result = cls._ps(ps, timeout=5)
                if not result.stdout.strip():
                    return {"error": "Could not read brightness. External monitor?"}
                data = json.loads(result.stdout)
                if isinstance(data, list):
                    data = data[0]
                return {"percent": data.get("CurrentBrightness", "Unknown")}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                result = cls._run(["brightnessctl", "g"])
                if result.returncode == 0:
                    curr = int(result.stdout.strip())
                    result2 = cls._run(["brightnessctl", "m"])
                    max_b = int(result2.stdout.strip())
                    return {"percent": round((curr / max_b) * 100, 1)}
            except:
                pass
            try:
                result = cls._run(["xrandr", "--verbose"])
                match = re.search(r'Brightness: (\d+\.\d+)', result.stdout)
                if match:
                    return {"percent": round(float(match.group(1)) * 100, 1)}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Brightness not supported on {cls.SYSTEM}"}

    @classmethod
    def set_brightness(cls, level: int) -> Dict:
        level = max(0, min(100, level))
        if cls.SYSTEM == "Windows":
            try:
                ps = (f'$monitor = Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods; '
                      f'$monitor.WmiSetBrightness(1, {level})')
                cls._ps(ps, timeout=5)
                return {"success": True, "level": level}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                cls._run(["brightnessctl", "set", f"{level}%"], check=True)
                return {"success": True, "level": level}
            except:
                try:
                    result = cls._run(["xrandr"])
                    output = result.stdout.split('\n')[0].split(' ')[0]
                    cls._run(["xrandr", "--output", output, "--brightness", str(level / 100)])
                    return {"success": True, "level": level}
                except Exception as e:
                    return {"error": str(e)}
        return {"error": f"Set brightness not supported on {cls.SYSTEM}"}

    # ── WiFi ────────────────────────────────────────────────
    @classmethod
    def get_wifi_networks(cls) -> List[Dict]:
        if cls.SYSTEM == "Windows":
            try:
                ps = 'netsh wlan show networks mode=Bssid | Out-String'
                result = cls._ps(ps, timeout=15)
                lines = result.stdout.split('\n')
                networks = []
                current = {}
                for line in lines:
                    line = line.strip()
                    if line.startswith("SSID"):
                        if current:
                            networks.append(current)
                        current = {"ssid": line.split(":", 1)[1].strip(),
                                   "signal": "Unknown", "security": "Unknown"}
                    elif "Signal" in line and current:
                        current["signal"] = line.split(":", 1)[1].strip()
                    elif "Authentication" in line and current:
                        current["security"] = line.split(":", 1)[1].strip()
                if current:
                    networks.append(current)
                return networks
            except Exception as e:
                return [{"error": str(e)}]
        elif cls.SYSTEM == "Linux":
            try:
                result = cls._run(["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi"])
                networks = []
                for line in result.stdout.strip().split('\n'):
                    if not line:
                        continue
                    parts = line.split(':')
                    networks.append({
                        "ssid": parts[0] if parts[0] else "Hidden",
                        "signal": parts[1] + "%" if len(parts) > 1 and parts[1] else "Unknown",
                        "security": parts[2] if len(parts) > 2 and parts[2] else "Open"
                    })
                return networks
            except Exception as e:
                return [{"error": str(e)}]
        return [{"error": f"WiFi scan not supported on {cls.SYSTEM}"}]

    @classmethod
    def connect_wifi(cls, ssid: str, password: Optional[str] = None) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                result = cls._run(["netsh", "wlan", "show", "profile", f"name={ssid}"])
                profile_exists = "not found" not in result.stdout.lower()

                if not profile_exists:
                    if not password:
                        return {"error": "Password required for new network", "needs_password": True}
                    # Build XML profile
                    xml_lines = [
                        '<?xml version="1.0"?>',
                        '<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">',
                        f'    <name>{ssid}</name>',
                        '    <SSIDConfig><SSID><name>' + ssid + '</name></SSID></SSIDConfig>',
                        '    <connectionType>ESS</connectionType>',
                        '    <connectionMode>auto</connectionMode>',
                        '    <MSM>',
                        '        <security>',
                        '            <authEncryption>',
                        '                <authentication>WPA2PSK</authentication>',
                        '                <encryption>AES</encryption>',
                        '                <useOneX>false</useOneX>',
                        '            </authEncryption>',
                        '            <sharedKey>',
                        '                <keyType>passPhrase</keyType>',
                        '                <protected>false</protected>',
                        '                <keyMaterial>' + password + '</keyMaterial>',
                        '            </sharedKey>',
                        '        </security>',
                        '    </MSM>',
                        '</WLANProfile>'
                    ]
                    profile_path = Path.home() / f".orbiton_wifi_{ssid.replace(' ', '_')}.xml"
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(xml_lines))
                    cls._run(["netsh", "wlan", "add", "profile", f"filename={profile_path}"])

                cls._run(["netsh", "wlan", "connect", f"name={ssid}"])
                return {"success": True, "ssid": ssid}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                if password:
                    cls._run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], check=True)
                else:
                    cls._run(["nmcli", "dev", "wifi", "connect", ssid], check=True)
                return {"success": True, "ssid": ssid}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"WiFi connect not supported on {cls.SYSTEM}"}

    # ── Bluetooth ───────────────────────────────────────────
    @classmethod
    def get_bluetooth_devices(cls) -> List[Dict]:
        if cls.SYSTEM == "Windows":
            try:
                ps = ('Get-PnpDevice -Class Bluetooth | '
                      'Where-Object {$_.FriendlyName -and $_.FriendlyName -notlike "*Radio*"} | '
                      'Select-Object FriendlyName, Status | ConvertTo-Json')
                result = cls._ps(ps, timeout=5)
                if not result.stdout.strip():
                    return [{"error": "No Bluetooth devices found"}]
                data = json.loads(result.stdout)
                if isinstance(data, dict):
                    data = [data]
                return [{"name": d.get("FriendlyName", "Unknown"),
                         "status": d.get("Status", "Unknown")} for d in data]
            except Exception as e:
                return [{"error": str(e)}]
        elif cls.SYSTEM == "Linux":
            try:
                result = cls._run(["bluetoothctl", "devices"])
                devices = []
                for line in result.stdout.strip().split('\n'):
                    parts = line.split(' ', 2)
                    if len(parts) >= 3:
                        devices.append({"name": parts[2], "status": "Paired"})
                return devices
            except Exception as e:
                return [{"error": str(e)}]
        return [{"error": f"Bluetooth not supported on {cls.SYSTEM}"}]

    @classmethod
    def toggle_bluetooth(cls, enable: bool) -> Dict:
        if cls.SYSTEM == "Windows":
            try:
                bt_tool = shutil.which("btpair.exe") or shutil.which("BluetoothCommandLineTools")
                if bt_tool:
                    action = "enable" if enable else "disable"
                    cls._run([bt_tool, action])
                    return {"success": True, "enabled": enable}
                return {"success": False, "error": "Bluetooth toggle requires admin rights on Windows. Use Settings or install Bluetooth command-line tools."}
            except Exception as e:
                return {"error": str(e)}
        elif cls.SYSTEM == "Linux":
            try:
                action = "power on" if enable else "power off"
                cls._run(["bluetoothctl", action], check=True)
                return {"success": True, "enabled": enable}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Bluetooth toggle not supported on {cls.SYSTEM}"}

    # ── System Info ─────────────────────────────────────────
    @classmethod
    def get_system_info(cls) -> Dict:
        try:
            disk = shutil.disk_usage('/')
            mem = None
            cpu_pct = None
            if PSUTIL_AVAILABLE:
                mem = psutil.virtual_memory()
                cpu_pct = psutil.cpu_percent(interval=0.5)

            return {
                "platform": cls.SYSTEM,
                "cpu_percent": cpu_pct,
                "memory_used_gb": round(mem.used / (1024**3), 2) if mem else None,
                "memory_total_gb": round(mem.total / (1024**3), 2) if mem else None,
                "memory_percent": mem.percent if mem else None,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
            }
        except Exception as e:
            return {"error": str(e)}


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
        if path and os.path.exists(path):
            subprocess.Popen(["code", path], shell=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            msg = f"Opening project {name} in VS Code"
            self.ui.show_success(msg)
            self.speak(msg)
        else:
            self.ui.show_error(f"Project not found: {name}")
            self.speak(f"I could not find the project {name}.")

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

    def handle_kosmosic(self):
        self.open_chrome(KOSMOSIC_APP)
        msg = "Opening Kosmosic study dashboard. Time to grind."
        self.ui.show_success(msg)
        self.speak(msg)

    def handle_help(self):
        self.ui.show_help()
        self.speak("Here is the full command list. You can say search, youtube, calculate, weather, airport, track flight, metar, open files, navigate folders, open projects, run scripts, maps, street view, clipboard search, motivate me, status report, exam mode, kosmosic, who am I, tell me about, battery, volume, brightness, wifi, bluetooth, system, reboot, help, sleep, or wake.")

    def handle_reboot(self):
        self.speak("Rebooting Orbiton. See you in a moment.")
        self.ui.show_info("🔄 Rebooting...")
        time.sleep(1)
        subprocess.Popen([sys.executable, __file__], 
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


class IntentParser:
    """Extract intent using regex patterns + NLP normalization."""

    PATTERNS = [
        (r"^(?:search|google|look up|find)\s+(.+)", "search"),
        (r"^(?:youtube|yt)\s+(.+)", "youtube"),
        (r"^(?:calculate|compute|math|solve)\s+(.+)", "calculate"),
        (r"^(?:weather)(?:\s+(?:in|at|for)?\s*(.+))?", "weather"),
        (r"^(?:airport|airports?)(?:\s+(?:in|at|for)?\s*(.+))?", "airport"),
        (r"^(?:track|flight|status of)\s+(.+)", "track"),
        (r"^(?:metar|taf|aviation weather)\s+(.+)", "metar"),
        (r"^(?:open project|project)\s+(.+)", "project"),
        (r"^(?:run|execute|start)\s+(.+)", "run"),
        (r"^(?:go to|navigate to|folder|enter)\s+(.+)", "folder_nav"),
        (r"^(?:open|show|launch)\s+(.+)", "open_file"),
        (r"^(?:maps?|where is|locate)\s+(.+)", "maps"),
        (r"^(?:streetview|street view|random place|travel)", "streetview"),
        (r"^(?:clipboard|paste|search clipboard)(?:\s+(youtube|google))?", "clipboard"),
        (r"^(?:motivate|roast|insult|toxic|pep talk)", "motivate"),
        (r"^(?:status|stats|report|diagnostic)", "status"),
        (r"^(?:exam mode|focus mode|launch mode|exambored|exambord|exum mode|eggsam mode)", "exam_mode"),
        (r"^(?:what time|current time|time is it|tell me the time)", "time"),
        (r"^(?:kosmosic|study dashboard|open kosmosic|kosmic|cosmic|cosmosic|kozmosic)", "kosmosic"),
        (r"^(?:help|commands|what can you do|show commands|help me|hell|hellp|halp|helf|elpe)", "help"),
        (r"^(?:reboot|restart|reload|rekognize|reeboot|rebbot|rebote)", "reboot"),
        (r"^(?:who am i|about me|my info|what do you know about me|whoami|huami|hooami)", "whoami"),
        (r"^(?:tell me about|what is|who is|where is|how to|what are|who was|what was)\s+(.+)", "knowledge"),
        (r"^(?:sleep|go to sleep|shut down|power off)", "sleep"),
        (r"^(?:wake|wake up|start|go online|power on)", "wake"),
        # ─── DEVICE PATTERNS ───
        (r"^(?:battery|power level|how much battery|charge left|how charged|battery status|remaining battery|battery percent)\b", "battery"),
        (r"^(?:volume|how loud|sound level|mute|unmute|turn (up|down) the (volume|sound)|set (volume|sound)|make it (louder|quieter)|louder|quieter|turn (up|down))\b", "volume"),
        (r"^(?:brightness|screen (brightness|dim)|how bright|dim the screen|brighten|set brightness|turn (up|down) brightness)\b", "brightness"),
        (r"^(?:wifi|wi-fi|connect to (wifi|network)|list networks|available (wifi|networks)|scan (wifi|networks)|wifi (status|networks)|show (wifi|networks))\b", "wifi"),
        (r"^(?:bluetooth|bt|pair bluetooth|bluetooth devices|toggle bluetooth|turn (on|off) bluetooth|bluetooth (status|on|off))\b", "bluetooth"),
        (r"^(?:system (info|status)|cpu usage|memory usage|ram usage|disk (space|usage)|storage|device status|how is my (system|computer|pc)|computer status)\b", "system"),
    ]

    def parse(self, text: str) -> Optional[tuple]:
        text = text.lower().strip()
        for pattern, intent in self.PATTERNS:
            match = re.match(pattern, text)
            if match:
                arg = match.group(1) if match.lastindex else ""
                return intent, arg.strip()
        return None


def process_text(text: str, engine: CommandEngine, parser: IntentParser,
                 memory: UserMemory, voice: VoiceManager, ui: NeuroInterface, intel) -> tuple:
    """
    Process a text command.
    Returns: (success: bool, action: str)
    action can be: 'sleep', 'wake', or ''
    """
    # First, try to learn from the text
    if memory.learn(text):
        msg = "Got it. I will remember that."
        ui.show_success(msg)
        voice.speak(msg)
        return True, ""

    # Try NLP intelligence first
    nlp_result = intel.process(text)
    if nlp_result[0] == "time":
        engine.handle_time()
        return True, ""
    elif nlp_result[0] == "weather":
        engine.handle_weather(nlp_result[1] or "")
        return True, ""
    elif nlp_result[0] == "knowledge":
        ui.show_knowledge("Knowledge", nlp_result[1])
        voice.speak(nlp_result[1])
        return True, ""
    elif nlp_result[0] == "search":
        engine.handle_search(nlp_result[1])
        return True, ""
    elif nlp_result[0] == "device":
        device_type, args = nlp_result[1]
        handler = getattr(engine, f"handle_{device_type}", None)
        if handler:
            if args:
                handler(args)
            else:
                handler()
        else:
            ui.show_error(f"Unknown device handler: {device_type}")
        return True, ""

    # Fall back to regex parser
    result = parser.parse(text)
    if result:
        intent, arg = result
        ui.total_commands += 1

        handler = getattr(engine, f"handle_{intent}", None)
        if handler:
            if arg:
                ret = handler(arg)
            else:
                ret = handler()
            if ret == "sleep":
                return True, "sleep"
            elif ret == "wake":
                return True, "wake"
            return True, ""
        else:
            ui.show_error(f"No handler for intent: {intent}")
            return False, ""
    else:
        ui.show_error(f"Unrecognized command: '{text}'")
        voice.speak("I did not understand that command.")
        return False, ""


def main():
    ui = NeuroInterface()
    ui.clear()
    ui.show_boot_sequence()
    ui.show_banner()

    ui.headphone_name = get_connected_headphones()
    if ui.headphone_name:
        ui.show_info(f"🎧 Connected: {ui.headphone_name}")
    else:
        ui.show_info("🎧 No Bluetooth headset detected. Using default mic.")

    ui.show_command_table()

    # Initialize intelligence, voice and memory
    intel = get_intelligence()
    voice = VoiceManager(voice=CONFIG["voice"])
    memory = UserMemory(CONFIG["memory_file"])
    engine = CommandEngine(ui, voice, memory, intel)
    parser = IntentParser()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    ui.show_info("Calibrating for ambient noise... (stay quiet)")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    ui.show_info("Ready. Say TOKYO or press headset button to wake me.")
    voice.speak("Orbiton online. Say Tokyo or press your headset button to wake me.")

    consecutive_errors = 0
    asleep = True

    # Text input thread
    text_queue = queue.Queue()
    def text_input_loop():
        while True:
            try:
                typed = input("\n[text] > ")
                if typed.strip():
                    text_queue.put(typed.strip())
            except EOFError:
                break

    text_thread = threading.Thread(target=text_input_loop, daemon=True)
    text_thread.start()

    while True:
        try:
            # ─── 1. TEXT INPUT (never blocked by TTS) ─────────────────
            try:
                typed_cmd = text_queue.get_nowait()
                ui.show_heard(f"[typed] {typed_cmd}")
                if asleep:
                    if CONFIG["wake_word"] in typed_cmd.lower() or typed_cmd.lower() in ("wake", "wake up", "start"):
                        asleep = False
                        msg = "Tokyo online. What do you need?"
                        ui.show_success(msg)
                        voice.speak(msg)
                        remainder = re.sub(r"\b(tokyo|wake|start)\b", "", typed_cmd, flags=re.IGNORECASE).strip()
                        if remainder:
                            process_text(remainder, engine, parser, memory, voice, ui, intel)
                    else:
                        ui.show_info("💤 Sleeping. Say TOKYO or WAKE to wake.")
                else:
                    success, action = process_text(typed_cmd, engine, parser, memory, voice, ui, intel)
                    if action == "sleep":
                        asleep = True
                continue
            except queue.Empty:
                pass

            # ─── 2. TTS SILENCE WINDOW (voice only) ───────────────────
            if voice.is_listening_blocked():
                time.sleep(0.1)
                continue

            # ─── 3. VOICE INPUT ───────────────────────────────────────
            if asleep:
                ui.show_listening(active=False)
            else:
                ui.show_listening(active=True)

            with microphone as source:
                audio = recognizer.listen(
                    source,
                    timeout=CONFIG["audio_timeout"],
                    phrase_time_limit=CONFIG["phrase_limit"]
                )

            ui.show_info("Processing speech...")
            text = recognizer.recognize_google(audio)
            ui.show_heard(text)

            # Wake word check
            if asleep:
                normalized = intel.nlp.normalize(text)
                if CONFIG["wake_word"] in normalized or any(w in normalized for w in ["wake", "wake up", "start", "online"]):
                    asleep = False
                    msg = "Tokyo online. What do you need?"
                    ui.show_success(msg)
                    voice.speak(msg)
                    remainder = re.sub(r"\b(tokyo|wake|wake up|start|online)\b", "", text, flags=re.IGNORECASE).strip()
                    if remainder:
                        process_text(remainder, engine, parser, memory, voice, ui, intel)
                continue

            # Awake: process command
            success, action = process_text(text, engine, parser, memory, voice, ui, intel)
            if action == "sleep":
                asleep = True

        except sr.WaitTimeoutError:
            consecutive_errors += 1
            if consecutive_errors > 3:
                ui.show_info("Still listening...")
                consecutive_errors = 0
        except sr.UnknownValueError:
            ui.show_error("Could not understand audio")
            consecutive_errors += 1
        except sr.RequestError as e:
            ui.show_error(f"Speech API error: {e}")
            consecutive_errors += 1
            time.sleep(2)
        except Exception as e:
            ui.show_error(f"Unexpected error: {e}")
            consecutive_errors += 1
            time.sleep(1)

        if consecutive_errors > CONFIG["max_errors_before_reset"]:
            ui.show_info("Resetting audio engine...")
            consecutive_errors = 0
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Orbiton shutting down. Stay toxic.\n")
