"""Test VS Code project launching and failure reporting."""
from unittest.mock import patch


def test_open_known_project(engine):
    with patch("stag.commands.subprocess.Popen") as mock_popen, \
         patch("stag.commands.os.path.exists", return_value=True), \
         patch("stag.commands.shutil.which", return_value="C:/VSCode/Code.exe"):
        engine.handle_project("hex link")

    mock_popen.assert_called_once()
    args = mock_popen.call_args.args[0]
    assert args[0].lower().endswith("code.exe")
    assert "hex-link" in args[1].lower()


def test_open_project_reports_missing_editor(engine):
    with patch("stag.commands.os.path.exists", return_value=True), \
         patch("stag.commands.shutil.which", return_value=None):
        engine.handle_project("hex link")

    engine.ui.show_error.assert_called_once_with(
        "VS Code was not found. Install it or add its CLI to PATH."
    )
    engine.voice.speak.assert_called_with("I could not find Visual Studio Code.")


def test_open_unknown_project_shows_error(engine):
    engine.handle_project("unknown_project_xyz")
    engine.ui.show_error.assert_called_once_with(
        "Project not found: unknown_project_xyz"
    )
    engine.voice.speak.assert_called_with(
        "I could not find the project unknown_project_xyz."
    )
