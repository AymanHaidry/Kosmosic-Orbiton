"""Terminal presentation layer."""
import os
import platform
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .config import ALL_COMMANDS

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    Console = Panel = Text = Table = box = None
    RICH_AVAILABLE = False

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
            print("\nCommands: search, youtube, calculate, weather, airport, track, metar, open, run, motivate, streetview, maps, clipboard, status, exam mode, help, reboot, who am i, sleep, wake, tell me about")
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


