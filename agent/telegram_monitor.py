"""Integration with the Telegram MCP server."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


try:
    from mcp import ClientSession
except ImportError:  # pragma: no cover - optional dependency
    ClientSession = None  # type: ignore


@dataclass
class TelegramMessage:
    id: int
    date: str
    text: str
    sender: Optional[str]


class TelegramMonitor:
    """High level wrapper around the telegram-mcp server."""

    def __init__(self, server_url: str, api_key: Optional[str], chat_id: str) -> None:
        if ClientSession is None:
            raise ImportError(
                "The 'mcp' package is required to connect to the Telegram MCP server. Install it with 'pip install mcp'."
            )
        self.server_url = server_url
        self.api_key = api_key
        self.chat_id = chat_id

    async def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
        async with await ClientSession.connect(self.server_url, extra_headers=headers) as session:
            response = await session.call_tool(tool_name, arguments)
            if isinstance(response, dict):
                return response
            raise RuntimeError("Unexpected response from MCP server")

    async def fetch_messages(self, since_id: Optional[int] = None, limit: int = 50) -> List[TelegramMessage]:
        payload = {"chat_id": self.chat_id, "limit": limit}
        if since_id is not None:
            payload["offset_id"] = since_id

        # telegram-mcp exposes `list_messages` by default. This block keeps compatibility with
        # potential alternative tool names such as `get_messages`.
        try:
            raw = await self._call_tool("list_messages", payload)
        except Exception:
            raw = await self._call_tool("get_messages", payload)

        items = raw.get("messages", raw)
        messages: List[TelegramMessage] = []
        for item in items:
            message_id = int(item.get("id") or item.get("message_id"))
            text = item.get("text", "") or ""
            if not text:
                continue
            messages.append(
                TelegramMessage(
                    id=message_id,
                    date=item.get("date", ""),
                    text=text,
                    sender=item.get("sender"),
                )
            )
        messages.sort(key=lambda message: message.id)
        return messages

    def fetch_messages_sync(self, since_id: Optional[int] = None, limit: int = 50) -> List[TelegramMessage]:
        return asyncio.run(self.fetch_messages(since_id=since_id, limit=limit))
