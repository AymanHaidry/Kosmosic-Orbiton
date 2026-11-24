"""Operating-system and hardware integrations."""
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False


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
            return name2 or None
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

    if system == "Darwin":
        try:
            result = subprocess.run(
                ["system_profiler", "SPBluetoothDataType", "-json"],
                capture_output=True, text=True, timeout=5
            )
            data = json.loads(result.stdout)
            if isinstance(data, list):
                devices = data
            elif isinstance(data, dict):
                devices = data.get("SPBluetoothDataType", [])
            else:
                devices = []

            for item in devices:
                if not isinstance(item, dict):
                    continue
                for name, details in item.items():
                    if not isinstance(details, dict):
                        continue
                    connected = str(details.get("device_connected", "")).strip().lower()
                    supported_name = any(
                        token in name.lower()
                        for token in ("jbl", "headphone", "earbud", "airpods", "sony", "bose")
                    )
                    if connected == "yes" and supported_name:
                        return name
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

    elif system == "Linux":
        try:
            result = subprocess.run(
                ["bluetoothctl", "info"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if "Name:" in line:
                    name = line.split("Name:", 1)[1].strip()
                    if any(
                        token in name.lower()
                        for token in ("jbl", "headphone", "earbud", "airpods", "sony", "bose")
                    ):
                        return name
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

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
                cls._run(["amixer", "set", "Master", f"{level}%"])
                return {"success": True, "level": level}
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Volume control not supported on {cls.SYSTEM}"}
