"""Minimal tool registry/queue for selecting derived tools on demand."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolRequest:
    name: str
    reason: str
    priority: int = 0


DEFAULT_TOOLS = {
    "compress": "TOOLS.compression_tool",
    "decompress": "TOOLS.compression_tool",
    "derive_views": "LAB.derived_views",
    "compare": "LAB.comparator",
}


def plan_tools(needs: list[str]) -> list[ToolRequest]:
    queue: list[ToolRequest] = []
    for need in needs:
        if need in DEFAULT_TOOLS:
            queue.append(ToolRequest(need, f"required for {need}", priority=0))
    return queue
