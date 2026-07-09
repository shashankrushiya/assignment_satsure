from __future__ import annotations

import json
from uuid import uuid4
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.ui.config.settings import load_ui_settings


def _post_raw(base_url: str, payload: dict, submission_id: str | None = None):
    headers = {"Content-Type": "application/json"}
    if submission_id:
        headers["X-Submission-Id"] = submission_id
    request = Request(
        f"{base_url}/api/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    return urlopen(request, timeout=5)


def test_missing_fields_are_rejected():
    settings = load_ui_settings()
    payload = {
        "account_id": "98765",
        "account_email": "test123@gmail.com",
        "start_date": "2024-03-15T10:30:00+05:30",
        "end_date": "2024-03-15T10:32:00+05:30",
        "locale": "en-IN",
        "text": "agile methodology",
        "completed": True,
    }

    try:
        _post_raw(settings.base_url, payload, uuid4().hex)
        raise AssertionError("Expected the backend to reject a payload with missing fields.")
    except HTTPError as exc:
        assert exc.code == 400


def test_invalid_data_types_are_rejected():
    settings = load_ui_settings()
    payload = {
        "account_id": "98765",
        "account_email": "test123@gmail.com",
        "start_date": "2024-03-15T10:30:00+05:30",
        "end_date": "2024-03-15T10:32:00+05:30",
        "locale": "en-IN",
        "text": "agile methodology",
        "suggestion_list": "agile methodology, agile methodology process, agile methodology process testing",
        "completed": "true",
    }

    try:
        _post_raw(settings.base_url, payload, uuid4().hex)
        raise AssertionError("Expected the backend to reject a payload with invalid types.")
    except HTTPError as exc:
        assert exc.code == 400


def test_unknown_submission_id_returns_not_found():
    settings = load_ui_settings()
    try:
        with urlopen(f"{settings.base_url}/api/responses/{uuid4().hex}", timeout=5):
            raise AssertionError("Expected a 404 for an unknown submission id.")
    except HTTPError as exc:
        assert exc.code == 404

