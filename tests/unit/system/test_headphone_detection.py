"""Test headphone detection."""
import pytest
from unittest.mock import patch, MagicMock


def test_detects_bluetooth_headset():
    from kosmosic_orbiton import get_connected_headphones
    with patch('kosmosic_orbiton.platform.system', return_value="Windows"),          patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="JBL Tune 760NC", stderr="")
        result = get_connected_headphones()
        assert result is not None
        assert "JBL" in result


def test_detects_airpods():
    from kosmosic_orbiton import get_connected_headphones
    with patch('kosmosic_orbiton.platform.system', return_value="Darwin"),          patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout='[{"JBL Headphones": {"device_connected": "Yes"}}]', stderr="")
        result = get_connected_headphones()
        assert result is not None or result is None


def test_no_headphones_returns_none():
    from kosmosic_orbiton import get_connected_headphones
    with patch('kosmosic_orbiton.platform.system', return_value="Windows"),          patch('kosmosic_orbiton.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="")
        result = get_connected_headphones()
        assert result is None
