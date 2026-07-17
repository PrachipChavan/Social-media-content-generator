"""
history.py — Content history management using a local JSON file.
"""

import json
import os
from datetime import datetime
from typing import Any

HISTORY_FILE = "content_history.json"
MAX_HISTORY_ITEMS = 50


def load_history() -> list[dict[str, Any]]:
    """Load content history from JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_to_history(
    platform: str,
    topic: str,
    tone: str,
    variations: list[str],
) -> None:
    """Save generated content to history."""
    history = load_history()

    entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "platform": platform,
        "topic": topic,
        "tone": tone,
        "variations": variations,
    }

    history.insert(0, entry)

    # Keep only the most recent items
    history = history[:MAX_HISTORY_ITEMS]

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not save history: {e}")


def delete_history_item(item_id: str) -> None:
    """Delete a single history item by ID."""
    history = load_history()
    history = [h for h in history if h.get("id") != item_id]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not update history: {e}")


def clear_history() -> None:
    """Clear all history."""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except IOError as e:
        print(f"Warning: Could not clear history: {e}")
