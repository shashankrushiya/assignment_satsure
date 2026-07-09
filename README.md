# Autocomplete Form SDET Assignment

This repository contains a fully runnable mock SUT plus Playwright and pytest automation for the autocomplete-form assignment.

## Setup

1. Create a virtual environment.

```powershell
python -m venv .venv
```

2. Activate it.

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies.

```powershell
pip install -r requirements.txt
```

4. Install Playwright browser binaries.

```powershell
playwright install
```

If your environment blocks the default Playwright cache directory, set the browser cache to the repo-local folder first:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD\.playwright-browsers"
playwright install
```

## Run

5. Run the UI suite alone.

```powershell
pytest tests/ui
```

6. Run the API suite alone.

```powershell
pytest tests/api
```

7. Run both suites together.

```powershell
pytest
```

8. Success is indicated by exit code `0` and pytest reporting all tests passed, with no failures or errors.

## Notes

- The backend starts and stops automatically from pytest fixtures, so no manual server launch is needed.
- The mock app is served locally at `http://127.0.0.1:8000` by default.
- Playwright uses a repo-local browser cache at `.playwright-browsers` when the default user-profile cache is not writable.
- Override the port or behavior with environment variables if needed:
  - `AUTOCOMPLETE_PORT`
  - `AUTOCOMPLETE_FILTER_MODE`
  - `AUTOCOMPLETE_HEADLESS`
  - `AUTOCOMPLETE_TIMEOUT_MS`

## Tested On

- OS: Microsoft Windows [Version 10.0.26200.8655]
- Python: 3.12.13
