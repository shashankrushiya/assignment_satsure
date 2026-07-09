from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import re
from threading import RLock
from typing import Any
from uuid import uuid4

from .config import SUGGESTIONS, Settings


LOCAL_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$"
)
BCP47_PATTERN = re.compile(
    r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$"
)


def create_submission_id() -> str:
    return uuid4().hex


def _normalize_text(value: str) -> str:
    return value.strip().casefold()


def matching_suggestions(value: str, mode: str) -> list[str]:
    normalized = _normalize_text(value)
    if not normalized:
        return []

    if mode == "anywhere":
        return [item for item in SUGGESTIONS if normalized in item.casefold()]

    return [item for item in SUGGESTIONS if item.casefold().startswith(normalized)]


def join_suggestions(value: str, mode: str) -> str:
    return ", ".join(matching_suggestions(value, mode))


def validate_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if not LOCAL_TIMESTAMP_PATTERN.match(value):
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_locale(value: Any) -> bool:
    return isinstance(value, str) and bool(BCP47_PATTERN.match(value))


@dataclass
class SubmissionStore:
    _items: dict[str, dict[str, Any]] = field(default_factory=dict)
    _lock: RLock = field(default_factory=RLock)

    def reset(self) -> None:
        with self._lock:
            self._items.clear()

    def save(self, submission_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._items[submission_id] = payload

    def get(self, submission_id: str) -> dict[str, Any] | None:
        with self._lock:
            payload = self._items.get(submission_id)
            if payload is None:
                return None
            return dict(payload)


store = SubmissionStore()


def validate_submission_payload(payload: Any, settings: Settings, filter_mode: str) -> tuple[bool, str]:
    required_fields = {
        "account_id",
        "account_email",
        "start_date",
        "end_date",
        "locale",
        "text",
        "suggestion_list",
        "completed",
    }

    if not isinstance(payload, dict):
        return False, "Request body must be a JSON object."

    payload_keys = set(payload.keys())
    if payload_keys != required_fields:
        missing = sorted(required_fields - payload_keys)
        extra = sorted(payload_keys - required_fields)
        problems = []
        if missing:
            problems.append(f"missing fields: {', '.join(missing)}")
        if extra:
            problems.append(f"unexpected fields: {', '.join(extra)}")
        return False, "; ".join(problems) or "Payload must contain only the FR-05 fields."

    if payload["account_id"] != settings.account_id:
        return False, "account_id does not match the authenticated session."
    if payload["account_email"] != settings.account_email:
        return False, "account_email does not match the authenticated session."
    if payload["locale"] != settings.locale:
        return False, "locale must match the configured browser locale."
    if not validate_locale(payload["locale"]):
        return False, "locale must be a well-formed IETF BCP 47 tag."
    if not validate_timestamp(payload["start_date"]):
        return False, "start_date must be a local ISO-8601 timestamp with offset."
    if not validate_timestamp(payload["end_date"]):
        return False, "end_date must be a local ISO-8601 timestamp with offset."
    if not isinstance(payload["text"], str) or not payload["text"].strip():
        return False, "text must be a non-empty string."
    if payload["text"] not in SUGGESTIONS:
        return False, "text must exactly match a valid suggestion."
    if not isinstance(payload["suggestion_list"], str):
        return False, "suggestion_list must be a comma-separated string."
    if not isinstance(payload["completed"], bool):
        return False, "completed must be a boolean."
    if payload["completed"] is not True:
        return False, "completed must be true on successful submission."

    expected_suggestions = join_suggestions(payload["text"], filter_mode)
    if payload["suggestion_list"] != expected_suggestions:
        return False, "suggestion_list does not match the filtered suggestions for the submitted value."

    return True, ""

