from __future__ import annotations

from playwright.sync_api import expect

from tests.ui.config.settings import load_ui_settings
from tests.ui.pages.autocomplete_page import AutocompletePage


def test_prefix_filter_keeps_only_prefix_matches(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.input.fill("agile methodology p")
    expect(form.suggestions).to_have_count(2)
    assert form.visible_suggestion_texts() == [
        "agile methodology process",
        "agile methodology process testing",
    ]


def test_match_anywhere_filter_keeps_contains_matches(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open(filter_mode="anywhere")

    form.input.fill("process")
    expect(form.suggestions).to_have_count(2)
    assert form.visible_suggestion_texts() == [
        "agile methodology process",
        "agile methodology process testing",
    ]


def test_clicking_suggestion_populates_input(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.click_suggestion("agile methodology process")
    expect(form.input).to_have_value("agile methodology process")

