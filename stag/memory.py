"""Local, user-controlled profile storage."""
import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, Optional

class UserMemory:
    """Stores user facts from statements like I am..., I like..., etc."""
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.legacy_filepath = Path.home() / ".neuro_link_memory.json"
        self.facts: Dict[str, str] = {}
        if not self.filepath.exists() and self.legacy_filepath.exists():
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(self.legacy_filepath, self.filepath)
            except OSError:
                pass
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.facts = json.load(f)
            except Exception:
                self.facts = {}

    def save(self):
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.facts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Memory save error] {e}")

    def learn(self, text: str) -> bool:
        """Extract I am / I like / My ... statements and store them."""
        text = text.lower().strip()
        patterns = [
            (r"(?:i am|i'm|my name is|call me)\s+(.+)", "name"),
            (r"(?:i like|i love|i enjoy)\s+(.+)", "likes"),
            (r"(?:i hate|i dislike)\s+(.+)", "dislikes"),
            (r"(?:i work as|i am a|my job is)\s+(.+)", "job"),
            (r"(?:i live in|i am from|my city is)\s+(.+)", "location"),
            (r"(?:my birthday is|i was born on)\s+(.+)", "birthday"),
            (r"(?:i study|my major is|i am studying)\s+(.+)", "study"),
            (r"(?:my goal is|i want to)\s+(.+)", "goals"),
        ]
        learned = False
        for pattern, key in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip().rstrip(".")
                if key in self.facts:
                    self.facts[key] += f", {value}"
                else:
                    self.facts[key] = value
                learned = True
        if learned:
            self.save()
        return learned

    def recall(self) -> str:
        if not self.facts:
            return "I do not know anything about you yet. Tell me something."
        parts = [f"Your {k} is {v}." for k, v in self.facts.items()]
        return " ".join(parts)

    def recall_one(self, key: str) -> Optional[str]:
        return self.facts.get(key.lower())


