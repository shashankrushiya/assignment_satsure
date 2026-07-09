from __future__ import annotations

from dataclasses import dataclass
import os


SUGGESTIONS = (
    "agile methodology",
    "agile methodology process",
    "agile methodology process testing",
)


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    filter_mode: str
    account_id: str
    account_email: str
    locale: str
    timezone: str

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


def _read_int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


def load_settings() -> Settings:
    filter_mode = os.getenv("AUTOCOMPLETE_FILTER_MODE", "prefix").strip().lower()
    if filter_mode not in {"prefix", "anywhere"}:
        raise ValueError(
            "AUTOCOMPLETE_FILTER_MODE must be either 'prefix' or 'anywhere'"
        )

    return Settings(
        host=os.getenv("AUTOCOMPLETE_HOST", "127.0.0.1").strip(),
        port=_read_int("AUTOCOMPLETE_PORT", 8000),
        filter_mode=filter_mode,
        account_id=os.getenv("AUTOCOMPLETE_ACCOUNT_ID", "98765").strip(),
        account_email=os.getenv("AUTOCOMPLETE_ACCOUNT_EMAIL", "test123@gmail.com").strip(),
        locale=os.getenv("AUTOCOMPLETE_LOCALE", "en-IN").strip(),
        timezone=os.getenv("AUTOCOMPLETE_TIMEZONE", "Asia/Kolkata").strip(),
    )

