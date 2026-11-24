"""Speech output and playback lifecycle."""
import asyncio
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
        """Background thread for TTS; recover cleanly from playback failures."""
        while True:
            text = self.tts_queue.get()
            if text is None:
                self.tts_queue.task_done()
                break
            self.tts_active.set()
            try:
                self._speak_now(text)
            except Exception:
                # A failed audio backend must not kill the worker thread.
                pass
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


