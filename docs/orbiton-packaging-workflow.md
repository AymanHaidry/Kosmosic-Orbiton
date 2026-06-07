# Orbiton Cross-Platform Packaging Workflow

## Overview

This workflow packages **Orbiton** (a Python desktop voice assistant) into downloadable executables for **macOS**, **Windows**, and **Linux** using **PyInstaller** with GitHub Actions for automated CI/CD builds.

> **Key Constraint**: PyInstaller is NOT a cross-compiler. You must build on each target OS.citeweb_search:2#0web_search:2#3 We use GitHub Actions runners (Windows, macOS, Ubuntu) to parallelize this.

---

## 1. Prerequisites

### Local Development Setup
```bash
# Clone the repo
git clone https://github.com/AymanHaidry/Kosmosic-Orbiton.git
cd Kosmosic-Orbiton

# Create virtual environment
python -m venv venv

# Activate (platform-specific)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

### Project Structure Assumptions
```
Kosmosic-Orbiton/
├── kosmosic_orbiton.py          # Main entry point
├── neuro_link_intel.py          # Intelligence module
├── requirements.txt             # Dependencies
├── assets/
│   ├── icon.ico                 # Windows icon (256x256)
│   ├── icon.icns                # macOS icon (1024x1024)
│   ├── icon.png                 # Linux icon (512x512)
│   └── splash.png               # Optional splash screen
├── config/
│   └── default_config.json      # Default configuration
└── .github/
    └── workflows/
        └── build.yml            # CI/CD workflow (created below)
```

---

## 2. PyInstaller Spec File (`orbiton.spec`)

Create this file in the repo root for consistent builds across platforms:

```python
# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, BUNDLE

# Platform detection
IS_WINDOWS = sys.platform.startswith('win')
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')

# Base paths
base_path = os.path.abspath('.')

# Data files to include
added_files = [
    ('config/default_config.json', 'config'),
    ('assets/splash.png', 'assets'),
]

# Hidden imports (for dynamic imports PyInstaller can't detect)
hidden_imports = [
    'speech_recognition',
    'edge_tts',
    'rich',
    'pyaudio',  # if using pyaudio for microphone
    'pyttsx3',  # if using pyttsx3 fallback
    'wikipedia',
    'requests',
    'json',
    'webbrowser',
    'subprocess',
    'os',
    'sys',
    'pathlib',
    'datetime',
    're',
    'math',
    'random',
    'urllib.parse',
]

# Platform-specific binaries
binaries = []
if IS_WINDOWS:
    # Add any required DLLs
    binaries.extend([])
elif IS_MACOS:
    # Add any required dylibs
    binaries.extend([])
elif IS_LINUX:
    # Add any required .so files
    binaries.extend([])

a = Analysis(
    ['kosmosic_orbiton.py'],
    pathex=[base_path],
    binaries=binaries,
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
    ],  # Exclude heavy libs not used by Orbiton to reduce size
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Platform-specific executable configuration
if IS_WINDOWS:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='Orbiton',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,  # Compress with UPX if available
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,  # Keep console for voice assistant output
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='assets/icon.ico',
        # Windows-specific: hide console option for production
        # console=False,  # Uncomment for GUI-only mode
    )

elif IS_MACOS:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='Orbiton',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # macOS apps typically don't show console
        disable_windowed_traceback=False,
        target_arch=None,  # Use 'universal2' for both Intel & Apple Silicon
        codesign_identity=None,  # Set to Apple Developer ID for signing
        entitlements_file=None,
        icon='assets/icon.icns',
    )

    # Create macOS .app bundle (required for proper macOS app behavior)
    app = BUNDLE(
        exe,
        name='Orbiton.app',
        icon='assets/icon.icns',
        bundle_identifier='com.kosmosic.orbiton',
        version='1.0.0',
        info_plist={
            'NSMicrophoneUsageDescription': 'Orbiton needs microphone access for voice commands.',
            'NSSpeechRecognitionUsageDescription': 'Orbiton uses speech recognition to process voice commands.',
            'LSBackgroundOnly': False,
            'LSUIElement': False,  # Set to True for menubar-only app
        },
    )

elif IS_LINUX:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='Orbiton',
        debug=False,
        bootloader_ignore_signals=False,
        strip=True,  # Strip symbols on Linux to reduce size
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,  # Linux users typically expect terminal output
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='assets/icon.png',
    )
```

---

## 3. GitHub Actions CI/CD Workflow (`.github/workflows/build.yml`)

```yaml
name: Build Orbiton Executables

on:
  push:
    branches: [ main, release/* ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Manual trigger

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build Windows executable
        run: |
          pyinstaller --clean orbiton.spec
        shell: cmd

      - name: Package Windows build
        run: |
          cd dist
          7z a -tzip Orbiton-Windows.zip Orbiton
        shell: cmd

      - name: Upload Windows artifact
        uses: actions/upload-artifact@v4
        with:
          name: Orbiton-Windows
          path: dist/Orbiton-Windows.zip
          retention-days: 30

  build-macos:
    runs-on: macos-latest  # Apple Silicon (M1/M2)
    strategy:
      matrix:
        arch: [arm64, x86_64]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          architecture: ${{ matrix.arch == 'x86_64' && 'x64' || 'arm64' }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build macOS app bundle
        run: |
          pyinstaller --clean orbiton.spec
        env:
          TARGET_ARCH: ${{ matrix.arch }}

      - name: Package macOS build
        run: |
          cd dist
          zip -r Orbiton-macOS-${{ matrix.arch }}.zip Orbiton.app

      - name: Upload macOS artifact
        uses: actions/upload-artifact@v4
        with:
          name: Orbiton-macOS-${{ matrix.arch }}
          path: dist/Orbiton-macOS-${{ matrix.arch }}.zip
          retention-days: 30

  build-linux:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [x86_64]
        # Add aarch64 if needed for ARM Linux (Raspberry Pi, etc.)
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y             libportaudio2             libportaudio-dev             pulseaudio             espeak             libespeak1

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build Linux executable
        run: |
          pyinstaller --clean orbiton.spec

      - name: Package Linux build
        run: |
          cd dist
          tar -czvf Orbiton-Linux.tar.gz Orbiton

      - name: Upload Linux artifact
        uses: actions/upload-artifact@v4
        with:
          name: Orbiton-Linux
          path: dist/Orbiton-Linux.tar.gz
          retention-days: 30

  release:
    needs: [build-windows, build-macos, build-linux]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            artifacts/Orbiton-Windows/Orbiton-Windows.zip
            artifacts/Orbiton-macOS-arm64/Orbiton-macOS-arm64.zip
            artifacts/Orbiton-macOS-x86_64/Orbiton-macOS-x86_64.zip
            artifacts/Orbiton-Linux/Orbiton-Linux.tar.gz
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 4. Platform-Specific Build Instructions

### Windows (Local Build)
```powershell
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build (one-folder mode - recommended for faster startup)
pyinstaller --clean orbiton.spec

# 3. Or build one-file executable (slower startup, easier distribution)
pyinstaller --onefile --icon=assets/icon.ico --name=Orbiton kosmosic_orbiton.py

# 4. Output is in `dist/Orbiton/` (folder) or `dist/Orbiton.exe` (onefile)

# 5. Optional: Create installer with Inno Setup or NSIS
# Download Inno Setup, create .iss script, compile to .exe installer
```

### macOS (Local Build)
```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build app bundle (creates Orbiton.app)
pyinstaller --clean --windowed --icon=assets/icon.icns --name=Orbiton kosmosic_orbiton.py

# 3. For Apple Silicon + Intel universal binary:
# Install universal2 Python, then:
pyinstaller --clean --target-arch universal2 --windowed orbiton.spec

# 4. Code signing (optional but recommended for distribution)
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/Orbiton.app

# 5. Notarization (required for Gatekeeper compliance)
xcrun notarytool submit dist/Orbiton.zip --apple-id "your@email.com" --team-id "TEAMID" --wait

# 6. Output: `dist/Orbiton.app` (drag to Applications folder)
```

### Linux (Local Build)
```bash
# 1. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y libportaudio2 libportaudio-dev pulseaudio espeak libespeak1

# 2. Install Python dependencies
pip install -r requirements.txt
pip install pyinstaller

# 3. Build
pyinstaller --clean orbiton.spec

# 4. Create AppImage (optional, for universal Linux distribution)
# Use appimagetool to package into .AppImage format
# Download from: https://appimage.github.io/

# 5. Or create .deb package (Debian/Ubuntu)
# Use dpkg-deb or checkinstall

# 6. Output: `dist/Orbiton/` folder or packaged format
```

---

## 5. Distribution Formats

| Platform | Recommended Format | Notes |
|----------|-------------------|-------|
| **Windows** | `.zip` (folder) or `.exe` (onefile) | Use Inno Setup for installer |
| **macOS** | `.app` bundle in `.zip` | Code sign + notarize for distribution |
| **Linux** | `.tar.gz` or `.AppImage` | AppImage works across distros |

### Optional: Create Installers

**Windows Installer (Inno Setup)** - `installer.iss`:
```ini
[Setup]
AppName=Orbiton
AppVersion=1.0
DefaultDirName={autopf}\Orbiton
DefaultGroupName=Orbiton
OutputDir=installer
OutputBaseFilename=Orbiton-Setup
SetupIconFile=assets\icon.ico

[Files]
Source: "dist\Orbiton\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Orbiton"; Filename: "{app}\Orbiton.exe"
Name: "{autodesktop}\Orbiton"; Filename: "{app}\Orbiton.exe"
```

**macOS DMG**:
```bash
# Create DMG for cleaner distribution
create-dmg   --volname "Orbiton Installer"   --window-pos 200 120   --window-size 800 400   --icon-size 100   --app-drop-link 600 185   "Orbiton.dmg"   "dist/Orbiton.app"
```

---

## 6. Handling Orbiton-Specific Dependencies

### Speech Recognition
```python
# In kosmosic_orbiton.py, ensure runtime path resolution:
import sys
import os

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

# Use base_path for any file operations
config_path = os.path.join(base_path, 'config', 'default_config.json')
```

### Audio Dependencies
```python
# Hidden imports for audio libraries (add to spec file):
hiddenimports = [
    'pyaudio',
    'speech_recognition',
    'edge_tts',
    'pyttsx3.drivers',
    'pyttsx3.drivers.sapi5',  # Windows TTS
    'pyttsx3.drivers.nsss',   # macOS TTS
    'pyttsx3.drivers.espeak', # Linux TTS
]
```

### Microphone Permissions
- **Windows**: No special permissions needed
- **macOS**: Add `NSMicrophoneUsageDescription` to Info.plist (see spec file above)
- **Linux**: Ensure user is in `audio` group: `sudo usermod -a -G audio $USER`

---

## 7. Testing the Build

```bash
# After building, test the executable:

# Windows
dist\Orbiton\Orbiton.exe
# or
dist\Orbiton.exe

# macOS
open dist/Orbiton.app
# or
dist/Orbiton

# Linux
./dist/Orbiton/Orbiton
```

**Common Issues & Fixes**:
1. **Missing DLLs/so/dylibs**: Add to `binaries` in spec file
2. **File not found errors**: Use `sys._MEIPASS` for bundled paths
3. **Audio not working**: Ensure PyAudio is included in hidden imports
4. **Slow startup (onefile)**: Use one-folder mode instead
5. **Antivirus false positive**: Code sign the executable

---

## 8. Size Optimization Tips

```python
# In spec file, exclude unused large libraries:
excludes=[
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'tkinter',
    'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
    'wx',
    'django',
    'flask',
    'sqlalchemy',
    'pytest',
    'unittest',
    'pydoc',
    'email',
    'html',
    'http',
    'xml',
    'lib2to3',
]
```

---

## 9. Complete Build Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] `orbiton.spec` file created and tested
- [ ] Icons created for all platforms (`.ico`, `.icns`, `.png`)
- [ ] `sys._MEIPASS` used for runtime file paths
- [ ] Hidden imports added for dynamic dependencies
- [ ] GitHub Actions workflow committed to `.github/workflows/build.yml`
- [ ] Test builds locally on each platform
- [ ] Code signing configured (macOS/Windows)
- [ ] README updated with download links
- [ ] Release created with all artifacts attached

---

## References

- PyInstaller Official Docs: https://pyinstaller.org/citeweb_search:2#2
- PyInstaller GitHub: https://github.com/pyinstaller/pyinstallerciteweb_search:2#7
- macOS Code Signing: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- GitHub Actions: https://docs.github.com/en/actions
