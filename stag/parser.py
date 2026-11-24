"""Command phrase parser."""
import re
from typing import Optional

class IntentParser:
    """Extract intent using regex patterns + NLP normalization."""

    PATTERNS = [
        (r"^(?:search|google|look up|find)\s+(.+)", "search"),
        (r"^(?:youtube|yt)\s+(.+)", "youtube"),
        (r"^(?:calculate|compute|math|solve)\s+(.+)", "calculate"),
        (r"^(?:weather)(?:\s+(?:in|at|for)?\s*(.+))?", "weather"),
        (r"^(?:airport|airports?)(?:\s+(?:in|at|for)?\s*(.+))?", "airport"),
        (r"^(?:track|flight|status of)\s+(.+)", "track"),
        (r"^(?:metar|taf|aviation weather)\s+(.+)", "metar"),
        (r"^(?:open project|project)\s+(.+)", "project"),
        (r"^(?:run|execute|start)\s+(.+)", "run"),
        (r"^(?:go to|navigate to|folder|enter)\s+(.+)", "folder_nav"),
        (r"^(?:open|show|launch)\s+(.+)", "open_file"),
        (r"^(?:maps?|where is|locate)\s+(.+)", "maps"),
        (r"^(?:streetview|street view|random place|travel)", "streetview"),
        (r"^(?:clipboard|paste|search clipboard)(?:\s+(youtube|google))?", "clipboard"),
        (r"^(?:motivate|roast|insult|toxic|pep talk)", "motivate"),
        (r"^(?:status|stats|report|diagnostic)", "status"),
        (r"^(?:exam mode|focus mode|launch mode|exambored|exambord|exum mode|eggsam mode)", "exam_mode"),
        (r"^(?:what time|current time|time is it|tell me the time)", "time"),
        (r"^(?:help|commands|what can you do|show commands|help me|hell|hellp|halp|helf|elpe)", "help"),
        (r"^(?:reboot|restart|reload|rekognize|reeboot|rebbot|rebote)", "reboot"),
        (r"^(?:who am i|about me|my info|what do you know about me|whoami|huami|hooami)", "whoami"),
        (r"^(?:tell me about|what is|who is|where is|how to|what are|who was|what was)\s+(.+)", "knowledge"),
        (r"^(?:sleep|go to sleep|shut down|power off)", "sleep"),
        (r"^(?:wake|wake up|start|go online|power on)", "wake"),
        # ─── DEVICE PATTERNS ───
        (r"^(?:battery|power level|how much battery|charge left|how charged|battery status|remaining battery|battery percent)\b", "battery"),
        (r"^(?:volume|how loud|sound level|mute|unmute|turn (up|down) the (volume|sound)|set (volume|sound)|make it (louder|quieter)|louder|quieter|turn (up|down))\b", "volume"),
        (r"^(?:brightness|screen (brightness|dim)|how bright|dim the screen|brighten|set brightness|turn (up|down) brightness)\b", "brightness"),
        (r"^(?:wifi|wi-fi|connect to (wifi|network)|list networks|available (wifi|networks)|scan (wifi|networks)|wifi (status|networks)|show (wifi|networks))\b", "wifi"),
        (r"^(?:bluetooth|bt|pair bluetooth|bluetooth devices|toggle bluetooth|turn (on|off) bluetooth|bluetooth (status|on|off))\b", "bluetooth"),
        (r"^(?:system (info|status)|cpu usage|memory usage|ram usage|disk (space|usage)|storage|device status|how is my (system|computer|pc)|computer status)\b", "system"),
    ]

    def parse(self, text: str) -> Optional[tuple]:
        text = text.lower().strip()
        for pattern, intent in self.PATTERNS:
            match = re.match(pattern, text)
            if match:
                arg = match.group(1) if match.lastindex else ""
                return intent, arg.strip()
        return None


