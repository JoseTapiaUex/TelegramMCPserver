"""REST client used to send approved posts to the backend."""
from __future__ import annotations

from typing import Any, Dict

import requests


class PostPublisher:
    def __init__(self, base_url: str, timeout: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/api/posts", json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
