# Architecture Discussion

## Why a mock SUT

The real `test.com` page and backend are not available in this workspace, so the assignment needs a local mock SUT to be executable. The mock mirrors the supplied HTML structure, implements the UI behavior in client-side JavaScript, and exposes a small REST backend that persists and retrieves responses.

## Test framework architecture

- `pytest` is used as the test runner and fixture engine.
- Playwright drives the UI against Chromium.
- The backend starts automatically from a session-scoped fixture, waits for a health check, and shuts down cleanly after the session.
- A function-scoped autouse fixture resets server state before each test to keep API and UI runs isolated.
- The browser context is configured with `locale="en-IN"` and `timezone_id="Asia/Kolkata"` so the target environment is simulated without needing a host-level locale change.

## Page Object Model

- The UI tests use a page object for the autocomplete form so raw selectors stay out of the test bodies.
- The page object centralizes field access, suggestion interaction, keyboard interaction, and submission actions.
- This makes the tests easier to read and reduces duplication across prefix, anywhere, and submission flows.

## Config strategy

- Backend behavior is controlled by environment variables for host, port, default filter mode, locale, account identity, and timezone.
- The UI test harness has its own config file for base URL, headless mode, and timeout values.
- The fixed port defaults to `127.0.0.1:8000`, with an environment variable override for conflict avoidance.

## CI readiness notes

- The suite does not require a manual server start.
- The backend is deterministic and self-contained, which makes it suitable for CI agents.
- Pinned dependencies keep the environment reproducible.
- The tests avoid shared-state dependence by keying persisted records to a submission id and clearing state between tests.

