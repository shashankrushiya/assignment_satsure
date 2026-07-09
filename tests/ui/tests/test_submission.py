from __future__ import annotations

import json
from datetime import datetime
from urllib.request import urlopen

from playwright.sync_api import expect

from tests.ui.config.settings import load_ui_settings
from tests.ui.pages.autocomplete_page import AutocompletePage


def _get_submission(submission_id: str, base_url: str) -> dict:
    with urlopen(f"{base_url}/api/responses/{submission_id}", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def test_successful_submission_persists_exact_payload(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.click_suggestion("agile methodology")
    form.click_next()

    expect(form.success_container).to_be_visible()
    expect(form.error_message).to_be_hidden()

    submission_id = page.evaluate("window.__AUTOCOMPLETE_STATE__.submissionId")
    assert isinstance(submission_id, str) and submission_id

    stored = _get_submission(submission_id, settings.base_url)
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
    assert stored["account_id"] == "98765"
    assert stored["account_email"] == "test123@gmail.com"
    assert stored["locale"] == "en-IN"
    assert stored["text"] == "agile methodology"
    assert stored["completed"] is True
    assert stored["suggestion_list"] == "agile methodology, agile methodology process, agile methodology process testing"
    assert datetime.fromisoformat(stored["start_date"])
    assert datetime.fromisoformat(stored["end_date"])


def test_invalid_input_shows_error_message(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.input.fill("agile method")
    form.click_next()

    expect(form.error_message).to_be_visible()
    expect(form.success_container).to_be_hidden()
