"""Persistence helpers to keep track of the last processed Telegram message."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class AgentState:
    last_message_id: Optional[int] = None
    last_run_at: Optional[str] = None

    @classmethod
    def from_file(cls, path: Path) -> "AgentState":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            last_message_id=data.get("last_message_id"),
            last_run_at=data.get("last_run_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "last_message_id": self.last_message_id,
            "last_run_at": self.last_run_at,
        }

    def save(self, path: Path) -> None:
        self.last_run_at = datetime.utcnow().isoformat()
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
