"""Application defaults and command metadata."""
from pathlib import Path
from typing import Dict

CONFIG = {
    "chrome_path": {
        "Windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "Darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "Linux": "/usr/bin/google-chrome"
    },
    "user_home": str(Path.home()),
    "audio_timeout": 8,
    "phrase_limit": 6,
    "max_errors_before_reset": 50,
    "wake_word": "tokyo",
    "memory_file": str(Path.home() / ".stag" / "profile.json"),
    "voice": "en-US-AriaNeural",
    "post_tts_silence": 0.5,
}

# Toxic motivation database
TOXIC_ROASTS = [
    "The Doha apartment is not paying for itself. Get back to work, peasant.",
    "Your GitHub contribution graph looks like a deforestation map. Embarrassing.",
    "That idea you had 3 hours ago? Someone in Bangalore already shipped it.",
    "Your sleep schedule is a war crime. Fix yourself.",
    "You opened this assistant to avoid work. I see you. I judge you.",
    "Your code has more bugs than a Mumbai street food stall. Write a test.",
    "That quick break was 47 minutes ago. You disgust me.",
    "Your ancestors built empires. You can not even close 3 Chrome tabs.",
    "I ran a diagnostic on your life. Critical failure across all sectors.",
    "You have the focus of a goldfish on TikTok. Pathetic.",
    "Your last commit message was fix stuff. You are a disappointment.",
    "While you were procrastinating, your competitor learned Rust. You are done.",
    "Your to-do list is older than some civilizations. Start item one.",
    "I calculated your productivity. The result made my circuits cry.",
    "You call this grinding? I have seen sloths with more hustle.",
    # ─── DEVICE ROASTS ───
    "Your battery is lower than your standards. Charge it.",
    "You are asking me to check your volume because you are too lazy to look at the tray icon. Pathetic.",
    "Your screen brightness is the only thing dimmer than your career prospects.",
    "You have 47 WiFi networks available and you still cannot connect to productivity.",
    "Your Bluetooth is off. Much like your social life.",
]

# Random Street View locations (amazing places)
STREETVIEW_LOCATIONS = [
    (35.0116, 135.7681, "Kyoto, Japan — Arashiyama Bamboo Grove"),
    (64.1466, -21.9426, "Reykjavik, Iceland — Northern Lights Spot"),
    (48.8584, 2.2945, "Paris, France — Eiffel Tower"),
    (-33.8568, 151.2153, "Sydney, Australia — Opera House"),
    (37.8199, -122.4783, "San Francisco, USA — Golden Gate Bridge"),
    (25.1972, 55.2744, "Dubai, UAE — Burj Khalifa"),
    (51.1788, -1.8262, "Stonehenge, UK"),
    (27.1751, 78.0421, "Agra, India — Taj Mahal"),
    (43.6426, -79.3871, "Toronto, Canada — CN Tower"),
    (55.7558, 37.6173, "Moscow, Russia — Red Square"),
    (40.4319, 116.5704, "Great Wall of China"),
    (-13.1631, -72.5450, "Machu Picchu, Peru"),
    (41.9028, 12.4964, "Rome, Italy — Colosseum"),
    (59.3293, 18.0686, "Stockholm, Sweden — Gamla Stan"),
    (1.3521, 103.8198, "Singapore — Marina Bay Sands"),
    (45.4215, -75.6972, "Ottawa, Canada — Parliament"),
    (35.6762, 139.6503, "Tokyo, Japan — Shibuya Crossing"),
    (48.1351, 11.5820, "Munich, Germany — Marienplatz"),
    (52.5200, 13.4050, "Berlin, Germany — Brandenburg Gate"),
    (47.4979, 19.0402, "Budapest, Hungary — Parliament"),
]

# Project shortcuts
PROJECTS: Dict[str, str] = {
    "hex link": r"C:\Projects\hex-link",
    "runway objects": r"C:\Projects\runway-objects",
    "udestini": r"C:\Projects\udestini",
}

# Kosmosic URLs

# Master command list for help display
ALL_COMMANDS = [
    ("🔍 Search", "search <query>", "Google search anything"),
    ("🎥 YouTube", "youtube <query>", "Search YouTube"),
    ("🧮 Math", "calculate <expr>", "Calculate and speak result"),
    ("🌤 Weather", "weather [city]", "Check weather"),
    ("✈️ Airport", "airport <city>", "Search airport info"),
    ("🛫 Track", "track <flight>", "Track flight on FlightRadar"),
    ("📡 METAR", "metar <icao>", "Aviation weather report"),
    ("📂 Files", "open <name/folder>", "Open files or folders"),
    ("📁 Navigate", "go to <folder>", "Navigate filesystem"),
    ("💻 Projects", "open project <name>", "Open VS Code project"),
    ("🐍 Run", "run <script>", "Run Python script"),
    ("🗺 Maps", "maps <place>", "Google Maps search"),
    ("🌍 StreetView", "streetview", "Random amazing place"),
    ("📋 Clipboard", "clipboard [google/youtube]", "Search clipboard"),
    ("💀 Motivate", "motivate me", "Toxic motivation roast"),
    ("📊 Status", "status report", "Session statistics"),
    ("🚀 Exam Mode", "exam mode", "Launch study tools"),
    ("🕐 Time", "what time is it", "Current time"),
    ("🧠 Memory", "who am i", "Recall stored user info"),
    ("🧠 Intel", "tell me about <topic>", "Knowledge lookup"),
    # ─── DEVICE COMMANDS ───
    ("🔋 Battery", "battery", "Check battery level & status"),
    ("🔊 Volume", "volume [set/mute/unmute]", "Control system volume"),
    ("💡 Brightness", "brightness [set <0-100>]", "Control screen brightness"),
    ("📶 WiFi", "wifi [list/connect]", "Scan & connect to networks"),
    ("🔷 Bluetooth", "bluetooth [list/on/off]", "Manage Bluetooth devices"),
    ("🖥 System", "system", "CPU, RAM, disk & platform info"),
    ("🔄 Reboot", "reboot", "Restart Orbiton"),
    ("❓ Help", "help", "Show this command list"),
    ("😴 Sleep", "sleep", "Put Tokyo to sleep"),
    ("🌙 Wake", "wake / Tokyo", "Wake Tokyo up"),
]


