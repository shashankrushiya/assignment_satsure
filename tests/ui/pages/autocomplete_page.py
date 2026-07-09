from __future__ import annotations

from playwright.sync_api import expect

from .base_page import BasePage


class AutocompletePage(BasePage):
    @property
    def input(self):
        return self.page.locator("#input-field")

    @property
    def suggestions(self):
        return self.page.locator("ul.suggestions li")

    @property
    def next_button(self):
        return self.page.locator("#next-button")

    @property
    def error_message(self):
        return self.page.locator(".error-message")

    @property
    def success_container(self):
        return self.page.locator(".success-container")

    def open(self, filter_mode: str | None = None) -> None:
        suffix = ""
        if filter_mode:
            suffix = f"?filter_mode={filter_mode}"
        self.goto(f"/autocomplete-form{suffix}")
        expect(self.input).to_be_visible()

    def type_text(self, value: str) -> None:
        self.input.fill(value)

    def click_suggestion(self, text: str) -> None:
        self.page.get_by_text(text, exact=True).click()

    def visible_suggestion_texts(self) -> list[str]:
        return self.suggestions.all_inner_texts()

    def press_tab(self) -> None:
        self.page.keyboard.press("Tab")

    def press_enter(self) -> None:
        self.page.keyboard.press("Enter")

    def press_escape(self) -> None:
        self.page.keyboard.press("Escape")

    def click_next(self) -> None:
        self.next_button.click()

    def input_value(self) -> str:
        return self.input.input_value()

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()

    def is_success_visible(self) -> bool:
        return self.success_container.is_visible()
