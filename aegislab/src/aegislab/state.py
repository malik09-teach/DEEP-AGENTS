"""State definitions and schemas for DeltaChannel.

This module defines Pydantic models (or similar) that represent the
state exchanged between the sandboxed backend and the orchestrator.
Placeholder implementations are provided; replace with real logic as
needed.
"""

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class DeltaChannelState:
    """Simple container for channel state.

    Attributes
    ----------
    metadata: Dict[str, Any]
        Arbitrary metadata about the current run.
    payload: Any
        The actual data being passed.
    """
    metadata: Dict[str, Any]
    payload: Any

# Example schema placeholder
ExampleSchema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
    },
    "required": ["message", "timestamp"],
}
