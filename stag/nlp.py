"""Natural-language normalization and extraction for Stag."""
import re
from typing import Optional, Tuple

class NaturalLanguageProcessor:
    """Converts sloppy speech into structured intent + arguments."""

    # Contractions & slang → expanded form
    CONTRACTIONS = {
        "what's": "what is",
        "whats": "what is",
        "where's": "where is",
        "wheres": "where is",
        "how's": "how is",
        "hows": "how is",
        "who's": "who is",
        "whos": "who is",
        "it's": "it is",
        "its": "it is",
        "i'm": "i am",
        "im": "i am",
        "you're": "you are",
        "youre": "you are",
        "don't": "do not",
        "dont": "do not",
        "can't": "cannot",
        "cant": "cannot",
        "won't": "will not",
        "wont": "will not",
        "isn't": "is not",
        "isnt": "is not",
        "aren't": "are not",
        "arent": "are not",
        "wasn't": "was not",
        "wasnt": "was not",
        "didn't": "did not",
        "didnt": "did not",
        "hasn't": "has not",
        "hasnt": "has not",
        "haven't": "have not",
        "havent": "have not",
        "couldn't": "could not",
        "couldnt": "could not",
        "wouldn't": "would not",
        "wouldnt": "would not",
        "shouldn't": "should not",
        "shouldnt": "should not",
        "let's": "let us",
        "lets": "let us",
        "gimme": "give me",
        "gonna": "going to",
        "wanna": "want to",
        "gotta": "got to",
        "kinda": "kind of",
        "sorta": "sort of",
        "dunno": "do not know",
        "lemme": "let me",
        "tellem": "tell them",
    }

    # Filler words to strip
    FILLERS = ["um", "uh", "like", "you know", "i mean", "basically", "literally",
               "actually", "honestly", "seriously", "so", "well", "okay", "ok"]

    # Homophone corrections for common misheard commands
    HOMOPHONES = {
        "exambored": "exam mode",
        "exambord": "exam mode",
        "exambored": "exam mode",
        "exum mode": "exam mode",
        "eggsam mode": "exam mode",
        "hell": "help",
        "hellp": "help",
        "halp": "help",
        "helf": "help",
        "elpe": "help",
        "stutus": "status",
        "statas": "status",
        "stattus": "status",
        "stutus report": "status report",
        "metar": "metar",
        "meter": "metar",
        "meeter": "metar",
        "meytar": "metar",
        "flight radar": "flightradar",
        "flightrader": "flightradar",
        "street view": "streetview",
        "streetvue": "streetview",
        "strretview": "streetview",
        "clipbored": "clipboard",
        "clipbord": "clipboard",
        "clipbord": "clipboard",
        "motivait": "motivate",
        "motivete": "motivate",
        "motovate": "motivate",
        "rekognize": "reboot",
        "reeboot": "reboot",
        "rebbot": "reboot",
        "rebote": "reboot",
        "whoami": "who am i",
        "huami": "who am i",
        "hooami": "who am i",
        # ─── DEVICE HOMOPHONES ───
        "batery": "battery",
        "battry": "battery",
        "batry": "battery",
        "volum": "volume",
        "volium": "volume",
        "voolume": "volume",
        "brigtness": "brightness",
        "brighness": "brightness",
        "brite": "bright",
        "wify": "wifi",
        "wi fi": "wifi",
        "weefee": "wifi",
        "bluetoof": "bluetooth",
        "bluetooh": "bluetooth",
        "blutooth": "bluetooth",
        "blutuf": "bluetooth",
        "sysinfo": "system",
        "sys info": "system",
    }

    # ─── DEVICE COMMAND PATTERNS ───
    DEVICE_PATTERNS = {
        "battery": [
            r"battery",
            r"power level",
            r"how much battery",
            r"charge left",
            r"how charged",
            r"battery status",
            r"remaining battery",
            r"battery percent",
        ],
        "volume": [
            r"volume",
            r"how loud",
            r"sound level",
            r"mute",
            r"unmute",
            r"turn (up|down) the (volume|sound)",
            r"set (volume|sound)",
            r"make it (louder|quieter)",
            r"louder",
            r"quieter",
            r"turn (up|down)",
        ],
        "brightness": [
            r"brightness",
            r"screen (brightness|dim)",
            r"how bright",
            r"dim the screen",
            r"brighten",
            r"set brightness",
            r"turn (up|down) brightness",
        ],
        "wifi": [
            r"wifi",
            r"wi-fi",
            r"connect to (wifi|network)",
            r"list networks",
            r"available (wifi|networks)",
            r"scan (wifi|networks)",
            r"wifi (status|networks)",
            r"show (wifi|networks)",
        ],
        "bluetooth": [
            r"bluetooth",
            r"bt",
            r"pair bluetooth",
            r"bluetooth devices",
            r"toggle bluetooth",
            r"turn (on|off) bluetooth",
            r"bluetooth (status|on|off)",
        ],
        "system": [
            r"system (info|status)",
            r"cpu usage",
            r"memory usage",
            r"ram usage",
            r"disk (space|usage)",
            r"storage",
            r"device status",
            r"how is my (system|computer|pc)",
            r"computer status",
        ],
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        """Full pipeline: lowercase → expand contractions → strip fillers → correct homophones."""
        text = text.lower().strip()

        # Expand contractions
        for contraction, expansion in cls.CONTRACTIONS.items():
            text = re.sub(rf"\b{re.escape(contraction)}\b", expansion, text)

        # Strip filler words
        for filler in cls.FILLERS:
            text = re.sub(rf"\b{re.escape(filler)}\b", "", text)

        # Clean up double spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Correct homophones
        for wrong, right in cls.HOMOPHONES.items():
            text = re.sub(rf"\b{re.escape(wrong)}\b", right, text)

        return text

    @classmethod
    def extract_time_query(cls, text: str) -> bool:
        """Detect if user is asking for time in various ways."""
        time_patterns = [
            r"what\s+is\s+the\s+time",
            r"what\s+time\s+is\s+it",
            r"tell\s+me\s+the\s+time",
            r"current\s+time",
            r"time\s+check",
            r"what\s+time\s+do\s+we\s+have",
            r"do\s+you\s+know\s+the\s+time",
            r"whats\s+the\s+time",
            r"what\s+is\s+the\s+time\s+now",
            r"time\s+please",
        ]
        return any(re.search(p, text) for p in time_patterns)

    @classmethod
    def extract_weather_query(cls, text: str) -> Optional[str]:
        """Extract city from weather queries like 'what\'s the weather in doha'."""
        patterns = [
            r"what\s+is\s+the\s+weather\s+(?:in|at|for)?\s*(.+)",
            r"how\s+is\s+the\s+weather\s+(?:in|at|for)?\s*(.+)",
            r"weather\s+(?:in|at|for)\s+(.+)",
            r"whats\s+the\s+weather\s+(?:in|at|for)?\s*(.+)",
            r"tell\s+me\s+the\s+weather\s+(?:in|at|for)?\s*(.+)",
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip()
        return None

    @classmethod
    def extract_search_query(cls, text: str) -> Optional[str]:
        """Extract query from search-like questions."""
        patterns = [
            r"what\s+is\s+(.+)",
            r"who\s+is\s+(.+)",
            r"where\s+is\s+(.+)",
            r"how\s+do\s+you\s+(.+)",
            r"how\s+to\s+(.+)",
            r"why\s+is\s+(.+)",
            r"when\s+is\s+(.+)",
            r"tell\s+me\s+about\s+(.+)",
            r"what\s+are\s+(.+)",
            r"who\s+was\s+(.+)",
            r"what\s+was\s+(.+)",
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip()
        return None

    @classmethod
    def extract_device_command(cls, text: str) -> Optional[Tuple[str, str]]:
        """Extract (device_type, args) from device-related commands."""
        normalized = cls.normalize(text)
        for device, patterns in cls.DEVICE_PATTERNS.items():
            for pattern in patterns:
                if re.search(rf"\b{pattern}\b", normalized):
                    # Extract args: everything after the matched pattern
                    match = re.search(rf"\b{pattern}\b", normalized)
                    if match:
                        args = normalized[match.end():].strip()
                        return device, args
                    return device, ""
        return None

    @classmethod
    def extract_volume_level(cls, text: str) -> Optional[int]:
        """Extract a percentage or level from volume commands."""
        match = re.search(r'(\d+)(?:\s*%|\s+percent)?', text)
        if match:
            return int(match.group(1))
        # Word numbers
        word_map = {
            "zero": 0, "one": 10, "two": 20, "three": 30, "four": 40,
            "five": 50, "six": 60, "seven": 70, "eight": 80, "nine": 90,
            "ten": 100, "half": 50, "quarter": 25, "max": 100, "maximum": 100,
            "min": 0, "minimum": 0, "full": 100,
        }
        for word, val in word_map.items():
            if re.search(rf"\b{word}\b", text.lower()):
                return val
        return None

    @classmethod
    def extract_brightness_level(cls, text: str) -> Optional[int]:
        """Extract a percentage from brightness commands."""
        return cls.extract_volume_level(text)  # Same logic


