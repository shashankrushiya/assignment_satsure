from __future__ import annotations

from playwright.sync_api import expect

from tests.ui.config.settings import load_ui_settings
from tests.ui.pages.autocomplete_page import AutocompletePage


def test_tab_navigation_moves_focus_between_form_elements(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.press_tab()
    expect(form.input).to_be_focused()

    form.press_tab()
    expect(form.next_button).to_be_focused()


def test_enter_key_submits_selected_suggestion(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.click_suggestion("agile methodology")
    form.input.focus()
    form.press_enter()

    expect(form.success_container).to_be_visible()
    expect(form.error_message).to_be_hidden()


def test_escape_clears_input_and_restores_full_suggestion_list(page):
    settings = load_ui_settings()
    form = AutocompletePage(page, settings.base_url)
    form.open()

    form.input.fill("agile method")
    form.page.keyboard.press("Escape")

    expect(form.input).to_have_value("")
    expect(form.suggestions).to_have_count(3)

