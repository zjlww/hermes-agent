"""Per-execution terminal cwd override.

Cron jobs can run concurrently inside one gateway process.  Environment
variables are process-global, so job-local cwd state must live in a
ContextVar and fall back to TERMINAL_CWD only when no scoped override exists.
"""

from __future__ import annotations

import os
from contextvars import ContextVar, Token

_terminal_cwd_override: ContextVar[str | None] = ContextVar(
    "terminal_cwd_override",
    default=None,
)


def get_terminal_cwd(default: str | None = None) -> str | None:
    """Return the scoped terminal cwd, then TERMINAL_CWD, then *default*."""
    scoped = _terminal_cwd_override.get()
    if scoped:
        return scoped
    env_value = os.getenv("TERMINAL_CWD")
    if env_value:
        return env_value
    return default


def set_terminal_cwd(value: str | None) -> Token[str | None]:
    """Set a ContextVar terminal cwd override for the current execution."""
    return _terminal_cwd_override.set(value)


def reset_terminal_cwd(token: Token[str | None]) -> None:
    """Restore the terminal cwd override to its previous value."""
    _terminal_cwd_override.reset(token)
