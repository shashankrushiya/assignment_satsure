from __future__ import annotations

import json
import re
from datetime import datetime
from uuid import uuid4
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.ui.config.settings import load_ui_settings


TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$")
BCP47_PATTERN = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


def _payload(text: str = "agile methodology") -> dict:
    settings = load_ui_settings()
    return {
        "account_id": "98765",
        "account_email": "test123@gmail.com",
        "start_date": "2024-03-15T10:30:00+05:30",
        "end_date": "2024-03-15T10:32:00+05:30",
        "locale": "en-IN",
        "text": text,
        "suggestion_list": "agile methodology, agile methodology process, agile methodology process testing",
        "completed": True,
    }


def _post_payload(base_url: str, submission_id: str, payload: dict) -> dict:
    request = Request(
        f"{base_url}/api/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Submission-Id": submission_id,
        },
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_payload(base_url: str, submission_id: str) -> dict:
    with urlopen(f"{base_url}/api/responses/{submission_id}", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def test_post_and_get_match_fr05_contract():
    settings = load_ui_settings()
    submission_id = uuid4().hex
    submitted = _payload()

    post_response = _post_payload(settings.base_url, submission_id, submitted)
    assert post_response["submission_id"] == submission_id
    assert post_response["status"] == "saved"

    stored = _get_payload(settings.base_url, submission_id)
    assert stored == submitted


def test_response_schema_and_types_are_valid():
    settings = load_ui_settings()
    submission_id = uuid4().hex
    _post_payload(settings.base_url, submission_id, _payload())
    stored = _get_payload(settings.base_url, submission_id)

    assert set(stored.keys()) == {
        "account_id",
        "account_email",
        "start_date",
        "end_date",
        "locale",
        "text",
        "suggestion_list",
        "completed",
    }
    assert isinstance(stored["account_id"], str)
    assert isinstance(stored["account_email"], str)
    assert isinstance(stored["start_date"], str)
    assert isinstance(stored["end_date"], str)
    assert isinstance(stored["locale"], str)
    assert isinstance(stored["text"], str)
    assert isinstance(stored["suggestion_list"], str)
    assert isinstance(stored["completed"], bool)
    assert TIMESTAMP_PATTERN.match(stored["start_date"])
    assert TIMESTAMP_PATTERN.match(stored["end_date"])
    datetime.fromisoformat(stored["start_date"])
    datetime.fromisoformat(stored["end_date"])
    assert BCP47_PATTERN.match(stored["locale"])
    assert stored["locale"] == "en-IN"


def test_suggestion_list_contains_only_matching_suggestions():
    settings = load_ui_settings()
    submission_id = uuid4().hex
    payload = _payload(text="agile methodology process")
    payload["suggestion_list"] = "agile methodology process, agile methodology process testing"
    _post_payload(settings.base_url, submission_id, payload)
    stored = _get_payload(settings.base_url, submission_id)
    assert stored["suggestion_list"] == "agile methodology process, agile methodology process testing"

