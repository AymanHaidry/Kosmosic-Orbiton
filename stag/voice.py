"""Speech output and playback lifecycle."""
import asyncio
import base64
import tempfile
import os
import platform
import queue
import subprocess
import sys
import threading
import time

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    edge_tts = None
    EDGE_TTS_AVAILABLE = False

class VoiceManager:
    """Natural text-to-speech using edge-tts or system fallback."""
    def __init__(self, voice: str = "en-US-AriaNeural", post_tts_silence: float = 1.5):
        self.voice = voice
        self.tts_queue = queue.Queue()
        self.tts_active = threading.Event()
        self.post_tts_until = 0.0
        self.post_tts_silence = max(0.0, float(post_tts_silence))
        self.last_error = None
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._tts_worker, daemon=True)
        self._thread.start()

    def _tts_worker(self):
        """Background thread for TTS; recover cleanly from playback failures."""
        while True:
            text = self.tts_queue.get()
            if text is None:
                self.tts_queue.task_done()
                break
            self.tts_active.set()
            try:
                self._speak_now(text)
            except Exception as exc:
                # A failed audio backend must not kill the worker thread.
                self.last_error = f"Speech playback failed: {exc}"
                print(self.last_error, file=sys.stderr)
            finally:
                with self._lock:
                    self.post_tts_until = time.time() + self.post_tts_silence
                self.tts_active.clear()
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
                with tempfile.NamedTemporaryFile(
                    prefix="stag-tts-", suffix=".mp3", delete=False
                ) as temporary_audio:
                    mp3_path = temporary_audio.name
                try:
                    asyncio.run(self._edge_speak(text, mp3_path))
                    if sys.platform == "win32":
                        try:
                            import pygame
                            if not pygame.mixer.get_init():
                                pygame.mixer.init()
                            pygame.mixer.music.load(mp3_path)
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                time.sleep(0.05)
                        except ImportError as exc:
                            raise RuntimeError("pygame is required for Edge TTS playback on Windows") from exc
                    elif sys.platform == "darwin":
                        subprocess.run(["afplay", mp3_path], capture_output=True, timeout=120)
                    else:
                        subprocess.run(["mpg123", mp3_path], capture_output=True, timeout=120)
                    time.sleep(0.2)
                    return
                finally:
                    try:
                        os.remove(mp3_path)
                    except OSError as exc:
                        self.last_error = f"Could not remove temporary speech file: {exc}"
            except Exception as exc:
                self.last_error = f"Neural speech unavailable: {exc}"
        self._system_speak(text)

    async def _edge_speak(self, text: str, path: str):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(path)

    def _system_speak(self, text: str):
        if platform.system() == "Windows":
            encoded = base64.b64encode(text.encode("utf-16le")).decode("ascii")
            script = (
                "Add-Type -AssemblyName System.Speech; "
                "$bytes = [Convert]::FromBase64String('" + encoded + "'); "
                "$message = [Text.Encoding]::Unicode.GetString($bytes); "
                "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak($message)"
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                capture_output=True,
                timeout=120,
                check=False,
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


