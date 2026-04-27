from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

MAX_ENTRIES = 20
_FILENAME = "leaderboard.json"


def _data_path(root_dir: Path) -> Path:
    return root_dir / _FILENAME


def load_scores(root_dir: Path) -> list[dict]:
    """Load leaderboard entries from disk. Returns a list sorted by score descending."""
    path = _data_path(root_dir)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_score(root_dir: Path, score: int) -> list[dict]:
    """Append a new score entry, keep top MAX_ENTRIES, persist to disk, return updated list."""
    entries = load_scores(root_dir)
    new_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "score": score,
    }
    entries.append(new_entry)
    entries.sort(key=lambda e: e.get("score", 0), reverse=True)
    entries = entries[:MAX_ENTRIES]
    try:
        _data_path(root_dir).write_text(json.dumps(entries, indent=2), encoding="utf-8")
    except OSError:
        pass
    return entries
