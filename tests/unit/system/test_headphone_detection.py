"""Test cross-platform Bluetooth headphone detection."""
from unittest.mock import MagicMock, patch

from stag.device import get_connected_headphones


def test_detects_bluetooth_headset():
    with patch("stag.device.platform.system", return_value="Windows"), \
         patch("stag.device.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="JBL Tune 760NC", stderr="")
        assert get_connected_headphones() == "JBL Tune 760NC"


def test_detects_airpods_from_system_profiler_list():
    """Accept the list-shaped Bluetooth payload used by some macOS versions."""
    payload = '[{"JBL Headphones": {"device_connected": "Yes"}}]'
    with patch("stag.device.platform.system", return_value="Darwin"), \
         patch("stag.device.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=payload, stderr="")
        assert get_connected_headphones() == "JBL Headphones"


def test_detects_airpods_from_system_profiler_object():
    """Accept the documented system_profiler top-level dictionary shape."""
    payload = '{"SPBluetoothDataType": [{"AirPods Pro": {"device_connected": "Yes"}}]}'
    with patch("stag.device.platform.system", return_value="Darwin"), \
         patch("stag.device.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=payload, stderr="")
        assert get_connected_headphones() == "AirPods Pro"


def test_ignores_disconnected_bluetooth_devices():
    payload = '[{"Sony Headphones": {"device_connected": "No"}}]'
    with patch("stag.device.platform.system", return_value="Darwin"), \
         patch("stag.device.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=payload, stderr="")
        assert get_connected_headphones() is None


def test_no_headphones_returns_none():
    with patch("stag.device.platform.system", return_value="Windows"), \
         patch("stag.device.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="")
        assert get_connected_headphones() is None
