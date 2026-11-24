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
            if name2:
                return name2
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

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
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

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
                cls._run(["amixer", "set", "Master", f"{level}%"], check=True)
                return {"success": True, "level": level}
            except (OSError, subprocess.SubprocessError):
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
            except (OSError, subprocess.SubprocessError):
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
            except (OSError, subprocess.SubprocessError, ValueError) as exc:
                brightnessctl_error = str(exc)
            try:
                result = cls._run(["xrandr", "--verbose"])
                match = re.search(r'Brightness: (\d+\.\d+)', result.stdout)
                if match:
                    return {"percent": round(float(match.group(1)) * 100, 1)}
            except Exception as e:
                return {"error": f"brightnessctl: {brightnessctl_error}; xrandr: {e}"}
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
            except (OSError, subprocess.SubprocessError):
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


