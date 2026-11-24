"""Application lifecycle and voice/text input loop."""
import queue
import re
import threading
import time

import speech_recognition as sr

from .config import CONFIG
from .commands import CommandEngine
from .device import get_connected_headphones
from .intelligence import get_intelligence
from .memory import UserMemory
from .parser import IntentParser
from .ui import NeuroInterface
from .voice import VoiceManager

def process_text(text: str, engine: CommandEngine, parser: IntentParser,
                 memory: UserMemory, voice: VoiceManager, ui: NeuroInterface, intel) -> tuple:
    """
    Process a text command.
    Returns: (success: bool, action: str)
    action can be: 'sleep', 'wake', or ''
    """
    # First, try to learn from the text
    if memory.learn(text):
        msg = "Got it. I will remember that."
        ui.show_success(msg)
        voice.speak(msg)
        return True, ""

    # Try NLP intelligence first
    nlp_result = intel.process(text)
    if nlp_result[0] == "time":
        engine.handle_time()
        return True, ""
    elif nlp_result[0] == "weather":
        engine.handle_weather(nlp_result[1] or "")
        return True, ""
    elif nlp_result[0] == "knowledge":
        ui.show_knowledge("Knowledge", nlp_result[1])
        voice.speak(nlp_result[1])
        return True, ""
    elif nlp_result[0] == "search":
        engine.handle_search(nlp_result[1])
        return True, ""
    elif nlp_result[0] == "device":
        device_type, args = nlp_result[1]
        handler = getattr(engine, f"handle_{device_type}", None)
        if handler:
            if args:
                handler(args)
            else:
                handler()
        else:
            ui.show_error(f"Unknown device handler: {device_type}")
        return True, ""

    # Fall back to regex parser
    result = parser.parse(text)
    if result:
        intent, arg = result
        ui.total_commands += 1

        handler = getattr(engine, f"handle_{intent}", None)
        if handler:
            if arg:
                ret = handler(arg)
            else:
                ret = handler()
            if ret == "sleep":
                return True, "sleep"
            elif ret == "wake":
                return True, "wake"
            return True, ""
        else:
            ui.show_error(f"No handler for intent: {intent}")
            return False, ""
    else:
        ui.show_error(f"Unrecognized command: '{text}'")
        voice.speak("I did not understand that command.")
        return False, ""


def main():
    ui = NeuroInterface()
    ui.clear()
    ui.show_boot_sequence()
    ui.show_banner()

    ui.headphone_name = get_connected_headphones()
    if ui.headphone_name:
        ui.show_info(f"🎧 Connected: {ui.headphone_name}")
    else:
        ui.show_info("🎧 No Bluetooth headset detected. Using default mic.")

    ui.show_command_table()

    # Initialize intelligence, voice and memory
    intel = get_intelligence()
    voice = VoiceManager(voice=CONFIG["voice"])
    memory = UserMemory(CONFIG["memory_file"])
    engine = CommandEngine(ui, voice, memory, intel)
    parser = IntentParser()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    ui.show_info("Calibrating for ambient noise... (stay quiet)")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    ui.show_info("Ready. Say TOKYO or press headset button to wake me.")
    voice.speak("Orbiton online. Say Tokyo or press your headset button to wake me.")

    consecutive_errors = 0
    asleep = True

    # Text input thread
    text_queue = queue.Queue()
    def text_input_loop():
        while True:
            try:
                typed = input("\n[text] > ")
                if typed.strip():
                    text_queue.put(typed.strip())
            except EOFError:
                break

    text_thread = threading.Thread(target=text_input_loop, daemon=True)
    text_thread.start()

    while True:
        try:
            # ─── 1. TEXT INPUT (never blocked by TTS) ─────────────────
            try:
                typed_cmd = text_queue.get_nowait()
                ui.show_heard(f"[typed] {typed_cmd}")
                if asleep:
                    if CONFIG["wake_word"] in typed_cmd.lower() or typed_cmd.lower() in ("wake", "wake up", "start"):
                        asleep = False
                        msg = "Tokyo online. What do you need?"
                        ui.show_success(msg)
                        voice.speak(msg)
                        remainder = re.sub(r"\b(tokyo|wake|start)\b", "", typed_cmd, flags=re.IGNORECASE).strip()
                        if remainder:
                            process_text(remainder, engine, parser, memory, voice, ui, intel)
                    else:
                        ui.show_info("💤 Sleeping. Say TOKYO or WAKE to wake.")
                else:
                    success, action = process_text(typed_cmd, engine, parser, memory, voice, ui, intel)
                    if action == "sleep":
                        asleep = True
                continue
            except queue.Empty:
                pass

            # ─── 2. TTS SILENCE WINDOW (voice only) ───────────────────
            if voice.is_listening_blocked():
                time.sleep(0.1)
                continue

            # ─── 3. VOICE INPUT ───────────────────────────────────────
            if asleep:
                ui.show_listening(active=False)
            else:
                ui.show_listening(active=True)

            with microphone as source:
                audio = recognizer.listen(
                    source,
                    timeout=CONFIG["audio_timeout"],
                    phrase_time_limit=CONFIG["phrase_limit"]
                )

            ui.show_info("Processing speech...")
            text = recognizer.recognize_google(audio)
            ui.show_heard(text)

            # Wake word check
            if asleep:
                normalized = intel.nlp.normalize(text)
                if CONFIG["wake_word"] in normalized or any(w in normalized for w in ["wake", "wake up", "start", "online"]):
                    asleep = False
                    msg = "Tokyo online. What do you need?"
                    ui.show_success(msg)
                    voice.speak(msg)
                    remainder = re.sub(r"\b(tokyo|wake|wake up|start|online)\b", "", text, flags=re.IGNORECASE).strip()
                    if remainder:
                        process_text(remainder, engine, parser, memory, voice, ui, intel)
                continue

            # Awake: process command
            success, action = process_text(text, engine, parser, memory, voice, ui, intel)
            if action == "sleep":
                asleep = True

        except sr.WaitTimeoutError:
            consecutive_errors += 1
            if consecutive_errors > 3:
                ui.show_info("Still listening...")
                consecutive_errors = 0
        except sr.UnknownValueError:
            ui.show_error("Could not understand audio")
            consecutive_errors += 1
        except sr.RequestError as e:
            ui.show_error(f"Speech API error: {e}")
            consecutive_errors += 1
            time.sleep(2)
        except Exception as e:
            ui.show_error(f"Unexpected error: {e}")
            consecutive_errors += 1
            time.sleep(1)

        if consecutive_errors > CONFIG["max_errors_before_reset"]:
            ui.show_info("Resetting audio engine...")
            consecutive_errors = 0
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Orbiton shutting down. Stay toxic.\n")
