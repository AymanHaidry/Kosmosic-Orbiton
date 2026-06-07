#!/usr/bin/env python3
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧠 ORBITON INTELLIGENCE MODULE
  Natural language understanding & knowledge engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

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
        """Extract city from weather queries like 'what's the weather in doha'."""
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


# ─── MATH NORMALIZER ───────────────────────────────────────
class MathNormalizer:
    """Converts spoken math into safe Python expressions."""

    # Word numbers → digits
    WORD_NUMBERS = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
        "hundred": 100, "thousand": 1000, "million": 1000000,
    }

    # Spoken operators → Python symbols (multi-word first)
    SPOKEN_OPS = {
        "to the power of": "**",
        "divided by": "/",
        "over": "/",
        "times": "*",
        "into": "*",
        "multiplied by": "*",
        "minus": "-",
        "subtract": "-",
        "plus": "+",
        "add": "+",
        "mod": "%",
        "modulo": "%",
        "squared": "**2",
        "cubed": "**3",
    }

    @classmethod
    def words_to_number(cls, words: list) -> float:
        """Convert a list of word tokens to a number."""
        current = 0
        total = 0
        scale = 1

        for word in words:
            val = cls.WORD_NUMBERS.get(word)
            if val is None:
                continue
            if val == 100:
                current = max(1, current) * 100
            elif val >= 1000:
                total += current
                current = 0
                scale = val
            else:
                current += val

        return (total + current) * scale

    @classmethod
    def normalize(cls, text: str) -> str:
        """Full pipeline: strip 'calculate', word numbers → digits, spoken ops → symbols."""
        text = text.lower().strip()

        # Remove command prefix
        text = re.sub(r"^calculate\s+", "", text)

        # Multi-word operators first (order matters — longest first)
        for spoken, symbol in sorted(cls.SPOKEN_OPS.items(), key=lambda x: -len(x[0])):
            text = re.sub(rf"\b{re.escape(spoken)}\b", f" {symbol} ", text)

        # Single-char operators (e.g. "x" as multiply)
        text = re.sub(r"\bx\b", "*", text)

        # Word numbers → digits
        tokens = text.split()
        i = 0
        out_tokens = []
        while i < len(tokens):
            num_words = []
            while i < len(tokens) and tokens[i] in cls.WORD_NUMBERS:
                num_words.append(tokens[i])
                i += 1
            if num_words:
                out_tokens.append(str(cls.words_to_number(num_words)))
            if i < len(tokens):
                out_tokens.append(tokens[i])
                i += 1

        expr = " ".join(out_tokens)
        expr = re.sub(r"\s+", " ", expr).strip()

        # Collapse multiple operators
        expr = re.sub(r"([+\-*/%])\s+\1+", r"\1", expr)

        return expr

    @classmethod
    def safe_eval(cls, expr: str) -> str:
        """Evaluate only safe math. No variables, no calls, no imports."""
        if not expr:
            raise ValueError("Empty expression")

        # Whitelist: digits, operators, parentheses, decimal points, spaces
        if not re.match(r"^[0-9+\-*/%.()\s]+$", expr):
            raise ValueError(f"Unsafe characters in expression: {expr}")

        try:
            result = eval(expr, {"__builtins__": {}}, {})
        except Exception as e:
            raise ValueError(f"Math error: {e}")

        # Format nicely
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)


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
        action_type can be: 'command', 'knowledge', 'time', 'weather', 'search', 'unknown'
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

        # 3. Check if it's a general knowledge question
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

        # 4. Check for direct knowledge queries
        direct = self.knowledge.lookup(normalized)
        if direct:
            return "knowledge", direct

        return "unknown", normalized

    def get_random_intel(self) -> str:
        return self.wiki.get_random_fact()

    def get_intel_categories(self) -> List[str]:
        return self.knowledge.get_categories()


# ─── SINGLETON INSTANCE ──────────────────────────────────────
_intel = None

def get_intelligence() -> IntelligenceOrchestrator:
    global _intel
    if _intel is None:
        _intel = IntelligenceOrchestrator()
    return _intel
