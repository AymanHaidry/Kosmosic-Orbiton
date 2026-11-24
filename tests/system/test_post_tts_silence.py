"""Tests for the microphone cooldown after text-to-speech playback."""
import queue
import threading
from unittest.mock import patch
from kosmosic_orbiton import VoiceManager

def make_manager(silence=1.5):
 voice=VoiceManager.__new__(VoiceManager)
 voice.tts_queue=queue.Queue()
 voice.tts_active=threading.Event()
 voice.post_tts_until=0.0
 voice.post_tts_silence=silence
 voice._lock=threading.Lock()
 return voice

def test_microphone_blocked_during_tts():
 voice=make_manager(); voice.tts_active.set()
 assert voice.is_listening_blocked() is True

def test_microphone_blocked_during_cooldown():
 voice=make_manager(); voice.post_tts_until=101.5
 with patch("kosmosic_orbiton.time.time",return_value=101.0):
  assert voice.is_listening_blocked() is True

def test_microphone_unblocks_after_cooldown():
 voice=make_manager(); voice.post_tts_until=101.0
 with patch("kosmosic_orbiton.time.time",return_value=101.1):
  assert voice.is_listening_blocked() is False

def test_worker_starts_configured_cooldown():
 voice=make_manager(2.0); spoken=[]
 voice._speak_now=spoken.append
 voice.tts_queue.put("hello Orbiton"); voice.tts_queue.put(None)
 with patch("kosmosic_orbiton.time.time",return_value=50.0):
  voice._tts_worker()
  assert voice.post_tts_until==52.0
  assert voice.is_listening_blocked() is True
 assert spoken==["hello Orbiton"]
 assert not voice.tts_active.is_set()

def test_zero_second_cooldown_unblocks_immediately():
 voice=make_manager(0); voice._speak_now=lambda _text:None
 voice.tts_queue.put("hello"); voice.tts_queue.put(None)
 with patch("kosmosic_orbiton.time.time",return_value=50.0):
  voice._tts_worker()
  assert voice.is_listening_blocked() is False

def test_worker_recovers_from_tts_failure_and_finishes_queue():
    voice = make_manager(silence=1.0)

    def fail(_text):
        raise RuntimeError("audio backend failed")

    voice._speak_now = fail
    voice.tts_queue.put("hello")
    voice.tts_queue.put(None)

    with patch("kosmosic_orbiton.time.time", return_value=70.0):
        voice._tts_worker()

    assert voice.post_tts_until == 71.0
    assert not voice.tts_active.is_set()
    assert voice.tts_queue.unfinished_tasks == 0
