"""
Simple in-memory conversation memory, keyed by session_id.
Swap this for MongoDB later if you want persistence across server restarts —
same pattern you used in your attendance system project.
"""

import json
import os
from datetime import datetime

CONVERSATIONS_FILE = os.path.join(os.path.dirname(__file__), "data", "conversations.json")

_SESSIONS: dict[str, list[dict]] = {}


def get_history(session_id: str) -> list[dict]:
    return _SESSIONS.get(session_id, [])


def update_history(session_id: str, messages: list[dict]) -> None:
    _SESSIONS[session_id] = messages
    _persist(session_id, messages)


def _persist(session_id: str, messages: list[dict]) -> None:
    """Best-effort logging of conversations to a local JSON file."""
    try:
        log = []
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, "r") as f:
                log = json.load(f)

        log.append({
            "session_id": session_id,
            "message_count": len(messages),
            "updated_at": datetime.utcnow().isoformat(),
        })

        with open(CONVERSATIONS_FILE, "w") as f:
            json.dump(log[-200:], f, indent=2)  # keep last 200 entries
    except Exception:
        pass  # logging failures should never break the chat