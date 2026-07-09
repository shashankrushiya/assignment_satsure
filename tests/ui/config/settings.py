from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class UiSettings:
    base_url: str
    headless: bool
    timeout_ms: int


def _read_bool(name: str, default: str = "true") -> bool:
    raw = os.getenv(name, default).strip().lower()
    return raw not in {"0", "false", "no", "off"}


def _read_int(name: str, default: str) -> int:
    return int(os.getenv(name, default).strip())


def load_ui_settings() -> UiSettings:
    host = os.getenv("AUTOCOMPLETE_HOST", "127.0.0.1").strip()
    port = _read_int("AUTOCOMPLETE_PORT", "8000")
    return UiSettings(
        base_url=f"http://{host}:{port}",
        headless=_read_bool("AUTOCOMPLETE_HEADLESS", "true"),
        timeout_ms=_read_int("AUTOCOMPLETE_TIMEOUT_MS", "10000"),
    )

