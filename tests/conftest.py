from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".playwright-browsers"))

from app.config import load_settings  # noqa: E402
from tests.ui.config.settings import load_ui_settings  # noqa: E402


SETTINGS = load_settings()


def _health_url() -> str:
    return f"{SETTINGS.base_url}/health"


def _wait_for_health(timeout_seconds: float = 30.0) -> None:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urlopen(_health_url(), timeout=1) as response:
                if response.status == 200:
                    return
        except Exception as exc:  # pragma: no cover - startup retry path
            last_error = exc
            time.sleep(0.25)
    raise RuntimeError(f"Backend did not become healthy in time: {last_error}")


def _post_reset() -> None:
    request = Request(
        f"{SETTINGS.base_url}/test/reset",
        method="POST",
        data=b"{}",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=5) as response:
            if response.status != 200:
                raise RuntimeError("Reset endpoint returned a non-200 response.")
    except HTTPError as exc:  # pragma: no cover - defensive
        raise RuntimeError(f"Reset endpoint failed: {exc.code} {exc.reason}") from exc


@pytest.fixture(scope="session", autouse=True)
def mock_backend() -> None:
    env = os.environ.copy()
    env.setdefault("AUTOCOMPLETE_HOST", SETTINGS.host)
    env.setdefault("AUTOCOMPLETE_PORT", str(SETTINGS.port))
    env.setdefault("AUTOCOMPLETE_FILTER_MODE", SETTINGS.filter_mode)
    env.setdefault("AUTOCOMPLETE_ACCOUNT_ID", SETTINGS.account_id)
    env.setdefault("AUTOCOMPLETE_ACCOUNT_EMAIL", SETTINGS.account_email)
    env.setdefault("AUTOCOMPLETE_LOCALE", SETTINGS.locale)
    env.setdefault("AUTOCOMPLETE_TIMEZONE", SETTINGS.timezone)

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.server:app",
            "--host",
            SETTINGS.host,
            "--port",
            str(SETTINGS.port),
            "--log-level",
            "warning",
        ],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        creationflags=creationflags,
    )

    try:
        _wait_for_health()
        yield
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


@pytest.fixture(autouse=True)
def clear_store_before_each_test(mock_backend: None) -> None:
    _post_reset()


@pytest.fixture(scope="session")
def playwright_browser():
    ui_settings = load_ui_settings()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=ui_settings.headless)
        yield browser
        browser.close()


@pytest.fixture
def browser_context(playwright_browser):
    ui_settings = load_ui_settings()
    context = playwright_browser.new_context(
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        viewport={"width": 1440, "height": 960},
    )
    context.set_default_timeout(ui_settings.timeout_ms)
    yield context
    context.close()


@pytest.fixture
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()
