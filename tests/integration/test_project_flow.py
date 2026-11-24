"""End-to-end project launch flow tests."""
from unittest.mock import patch

from stag.app import process_text


def test_project_flow_known(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    with patch("stag.commands.subprocess.Popen") as mock_popen, \
         patch("stag.commands.os.path.exists", return_value=True), \
         patch("stag.commands.shutil.which", return_value="C:/VSCode/Code.exe"):
        success, action = process_text(
            "open project hex link",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )

    assert success is True
    assert action == ""
    mock_popen.assert_called_once()
    assert "hex-link" in mock_popen.call_args.args[0][1].lower()


def test_project_flow_unknown(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    success, action = process_text(
        "open project fake_project",
        engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
    )
    assert success is True
    assert action == ""
    mock_ui.show_error.assert_called_once()
