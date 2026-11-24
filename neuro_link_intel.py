#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 🧠 ORBITON INTELLIGENCE MODULE
 Natural language understanding & knowledge engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import ast
import math
import re
import json
import os
import random
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# ─── NLP: Normalize messy speech to clean commands ───────────
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
        "kosmic": "kosmosic",
        "cosmic": "kosmosic",
        "cosmosic": "kosmosic",
        "kozmosic": "kosmosic",
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


# ─── KNOWLEDGE ENGINE ────────────────────────────────────────
class KnowledgeEngine:
    """Looks up facts from local intel files and wikimedia dumps."""

    INTEL_DIR = Path.home() / ".neuro_link_intel"

    # Built-in mini knowledge bases
    BUILTIN_INTEL = {

    }

    def __init__(self):
        self.INTEL_DIR.mkdir(parents=True, exist_ok=True)
        self._load_all_intel()

    def _load_all_intel(self):
        """Load all intel files from disk."""
        self.knowledge = {}
        for key, data in self.BUILTIN_INTEL.items():
            self.knowledge[key] = data

        # Load user-created intel files
        for filepath in self.INTEL_DIR.glob("intel_*.json"):
            key = filepath.stem.replace("intel_", "")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.knowledge[key] = json.load(f)
            except Exception:
                pass

    def lookup(self, topic: str) -> Optional[str]:
        """Search all knowledge bases for a topic."""
        topic = topic.lower().strip()

        # Direct match in any knowledge base
        for kb_name, kb_data in self.knowledge.items():
            if isinstance(kb_data, dict):
                for key, value in kb_data.items():
                    if topic in key or key in topic:
                        return f"[{kb_name}] {value}"
            elif isinstance(kb_data, list):
                for item in kb_data:
                    if isinstance(item, dict) and topic in str(item).lower():
                        return f"[{kb_name}] {item}"

        # Fuzzy match: topic appears anywhere in keys
        for kb_name, kb_data in self.knowledge.items():
            if isinstance(kb_data, dict):
                for key, value in kb_data.items():
                    if any(word in key for word in topic.split()):
                        return f"[{kb_name}] {value}"

        return None

    def get_categories(self) -> List[str]:
        return list(self.knowledge.keys())

    def add_intel_file(self, name: str, data: Dict):
        """Add a new intel file to disk."""
        filepath = self.INTEL_DIR / f"intel_{name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.knowledge[name] = data


# ─── WIKIMEDIA SCRAPER ───────────────────────────────────────
class WikimediaScraper:
    """Scrapes wikimedia dumps for general knowledge."""

    DUMP_BASE = "https://dumps.wikimedia.org/other/mediawiki_content_current/"

    def __init__(self):
        self.cache_dir = Path.home() / ".neuro_link_wiki_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def search_topic(self, topic: str) -> Optional[str]:
        """Search for a topic in cached wikimedia data."""
        topic = topic.lower().replace(" ", "_")
        cache_file = self.cache_dir / f"{topic}.txt"

        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return f.read()[:500]  # Return first 500 chars

        # Try to fetch from Wikipedia API (simple REST)
        try:
            import urllib.request
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())
                extract = data.get("extract", "")
                if extract:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        f.write(extract)
                    return extract[:500]
        except Exception:
            pass

        return None

    def get_random_fact(self) -> str:
        """Return a random fact from built-in knowledge."""
        all_facts = []
        for kb in KnowledgeEngine.BUILTIN_INTEL.values():
            all_facts.extend(kb.values())
        return random.choice(all_facts) if all_facts else "I know nothing yet."


# ─── INTELLIGENCE ORCHESTRATOR ───────────────────────────────
class IntelligenceOrchestrator:
    """Main intelligence hub that combines NLP + Knowledge + Search."""

    def __init__(self):
        self.nlp = NaturalLanguageProcessor()
        self.knowledge = KnowledgeEngine()
        self.wiki = WikimediaScraper()

    def process(self, text: str) -> Tuple[str, Optional[str]]:
        """
        Process raw speech text.
        Returns: (action_type, data)
        action_type can be: 'command', 'knowledge', 'time', 'weather', 'search', 'device', 'unknown'
        data is the extracted argument or knowledge text.
        """
        normalized = self.nlp.normalize(text)

        # 1. Check if it's a time query
        if self.nlp.extract_time_query(normalized):
            return "time", None

        # 2. Check if it's a weather query
        weather_city = self.nlp.extract_weather_query(normalized)
        if weather_city:
            return "weather", weather_city

        # 3. Check device commands
        device_cmd = self.nlp.extract_device_command(normalized)
        if device_cmd:
            return "device", device_cmd  # (device_type, args)

        # 4. Check if it's a general knowledge question
        search_query = self.nlp.extract_search_query(normalized)
        if search_query:
            # Try local knowledge first
            local = self.knowledge.lookup(search_query)
            if local:
                return "knowledge", local
            # Try wikipedia
            wiki = self.wiki.search_topic(search_query)
            if wiki:
                return "knowledge", wiki
            # Fall back to Google search
            return "search", search_query

        # 5. Check for direct knowledge queries
        direct = self.knowledge.lookup(normalized)
        if direct:
            return "knowledge", direct

        return "unknown", normalized

    def get_random_intel(self) -> str:
        return self.wiki.get_random_fact()

    def get_intel_categories(self) -> List[str]:
        return self.knowledge.get_categories()


# ─── MATH NORMALIZER ─────────────────────────────────────────
class MathNormalizer:
    """Normalize spoken arithmetic and evaluate it with a strict AST allowlist."""
    REPLACEMENTS = {
        "multiplied by":"*", "divided by":"/", "to the power of":"**",
        "square root of":"math.sqrt(", "cube root of":"math.cbrt(",
        "factorial of":"math.factorial(", "percent of":"/100*",
        "squared":"**2", "cubed":"**3", "plus":"+", "minus":"-",
        "times":"*", "over":"/", "modulo":"%", "mod":"%",
        "percent":"/100", "pi":"math.pi", "e":"math.e", "x":"*",
    }
    WORD_NUMBERS = {
        "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,
        "seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,
        "thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,
        "eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,
        "fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,
        "hundred":100,"thousand":1000,
    }

    @classmethod
    def _replace_word_numbers(cls, expression):
        tokens, output, index = expression.split(), [], 0
        while index < len(tokens):
            if tokens[index] not in cls.WORD_NUMBERS:
                output.append(tokens[index]); index += 1; continue
            total = current = 0
            while index < len(tokens) and tokens[index] in cls.WORD_NUMBERS:
                value = cls.WORD_NUMBERS[tokens[index]]
                if value == 100: current = max(current, 1) * 100
                elif value == 1000: total += max(current, 1) * 1000; current = 0
                else: current += value
                index += 1
            output.append(str(total + current))
        return " ".join(output)

    @classmethod
    def normalize(cls, expr):
        """Convert spoken math into a compact expression for safe_eval()."""
        if not isinstance(expr, str): raise TypeError("Math expression must be text")
        expr = cls._replace_word_numbers(expr.lower().strip())
        for phrase, symbol in sorted(cls.REPLACEMENTS.items(), key=lambda item: -len(item[0])):
            expr = re.sub(rf"\b{re.escape(phrase)}\b", lambda _m, v=symbol: v, expr)
        expr = re.sub(r"\s+", "", expr)
        if expr.count("(") > expr.count(")"):
            expr += ")" * (expr.count("(") - expr.count(")"))
        return expr

    @classmethod
    def safe_eval(cls, expr):
        """Evaluate arithmetic without eval(), builtins, or arbitrary calls."""
        if not isinstance(expr, str) or not expr.strip(): raise ValueError("Empty expression")
        if len(expr) > 256: raise ValueError("Expression is too long")
        try: tree = ast.parse(expr, mode="eval")
        except (SyntaxError, ValueError) as exc: raise ValueError(f"Invalid math expression: {exc}") from exc
        if sum(1 for _ in ast.walk(tree)) > 64: raise ValueError("Expression is too complex")
        binary = {
            ast.Add:lambda a,b:a+b, ast.Sub:lambda a,b:a-b, ast.Mult:lambda a,b:a*b,
            ast.Div:lambda a,b:a/b, ast.FloorDiv:lambda a,b:a//b, ast.Mod:lambda a,b:a%b,
            ast.Pow:lambda a,b:a**b,
        }
        unary = {ast.UAdd:lambda x:+x, ast.USub:lambda x:-x}
        def checked(value):
            if isinstance(value,bool) or not isinstance(value,(int,float)): raise ValueError("Only numeric results are allowed")
            try: finite=math.isfinite(value)
            except (OverflowError,TypeError): finite=False
            if not finite or abs(value)>1e100: raise ValueError("Result is outside the supported range")
            return value
        def visit(node):
            if isinstance(node,ast.Expression): return visit(node.body)
            if isinstance(node,ast.Constant):
                if type(node.value) not in (int,float): raise ValueError("Only numeric literals are allowed")
                return checked(node.value)
            if isinstance(node,ast.BinOp):
                op=binary.get(type(node.op))
                if op is None: raise ValueError("Operator is not allowed")
                left,right=visit(node.left),visit(node.right)
                if isinstance(node.op,ast.Pow) and abs(right)>100: raise ValueError("Exponent is too large")
                return checked(op(left,right))
            if isinstance(node,ast.UnaryOp):
                op=unary.get(type(node.op))
                if op is None: raise ValueError("Unary operator is not allowed")
                return checked(op(visit(node.operand)))
            if isinstance(node,ast.Attribute):
                if isinstance(node.value,ast.Name) and node.value.id=="math" and node.attr in ("pi","e"):
                    return getattr(math,node.attr)
                raise ValueError("Math attribute is not allowed")
            if isinstance(node,ast.Call):
                if node.keywords: raise ValueError("Keyword arguments are not allowed")
                if isinstance(node.func,ast.Name) and node.func.id in ("abs","round"):
                    function=abs if node.func.id=="abs" else round
                    allowed=(1,) if node.func.id=="abs" else (1,2)
                    if len(node.args) not in allowed: raise ValueError("Invalid function arguments")
                elif (isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name)
                      and node.func.value.id=="math" and node.func.attr in ("sqrt","cbrt","factorial")):
                    function=getattr(math,node.func.attr,None)
                    if function is None or len(node.args)!=1: raise ValueError("Unsupported math function")
                else: raise ValueError("Function call is not allowed")
                args=[visit(arg) for arg in node.args]
                if isinstance(node.func,ast.Attribute) and node.func.attr=="factorial":
                    value=args[0]
                    if not isinstance(value,int) or value<0 or value>170:
                        raise ValueError("factorial() requires an integer from 0 to 170")
                return checked(function(*args))
            raise ValueError(f"Expression element is not allowed: {type(node).__name__}")
        try: return visit(tree)
        except ValueError: raise
        except Exception as exc: raise ValueError(f"Could not evaluate expression: {exc}") from exc


# ─── SINGLETON INSTANCE ──────────────────────────────────────
_intel = None

def get_intelligence() -> IntelligenceOrchestrator:
    global _intel
    if _intel is None:
        _intel = IntelligenceOrchestrator()
    return _intel
