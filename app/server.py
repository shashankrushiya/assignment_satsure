from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .config import load_settings, SUGGESTIONS
from .html import render_form_html
from .store import create_submission_id, store, validate_submission_payload


settings = load_settings()
app = FastAPI(title="Autocomplete Mock SUT", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/autocomplete-form", response_class=HTMLResponse)
def autocomplete_form(
    filter_mode: str | None = Query(default=None, alias="filter_mode"),
) -> HTMLResponse:
    mode = filter_mode or settings.filter_mode
    if mode not in {"prefix", "anywhere"}:
        raise HTTPException(status_code=400, detail="filter_mode must be prefix or anywhere")
    return HTMLResponse(render_form_html(settings, mode))


@app.post("/api/responses")
async def create_response(
    request: Request,
    x_submission_id: str | None = Header(default=None, alias="X-Submission-Id"),
    x_filter_mode: str | None = Header(default=None, alias="X-Filter-Mode"),
) -> JSONResponse:
    submission_id = x_submission_id or create_submission_id()
    try:
        payload = await request.json()
    except Exception as exc:  # pragma: no cover - invalid JSON path
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.") from exc

    if "submission_id" in payload:
        raise HTTPException(status_code=400, detail="submission_id must be provided in the X-Submission-Id header.")

    filter_mode = x_filter_mode or settings.filter_mode
    if filter_mode not in {"prefix", "anywhere"}:
        raise HTTPException(status_code=400, detail="X-Filter-Mode must be prefix or anywhere.")

    is_valid, message = validate_submission_payload(payload, settings, filter_mode)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    store.save(submission_id, payload)
    return JSONResponse(
        status_code=200,
        content={"submission_id": submission_id, "status": "saved"},
        headers={"X-Submission-Id": submission_id},
    )


@app.get("/api/responses/{submission_id}")
def get_response(submission_id: str) -> JSONResponse:
    payload = store.get(submission_id)
    if payload is None:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return JSONResponse(status_code=200, content=payload)


@app.post("/test/reset")
def reset_store() -> dict[str, str]:
    store.reset()
    return {"status": "reset"}


@app.get("/api/suggestions")
def get_suggestions() -> dict[str, object]:
    return {"suggestions": list(SUGGESTIONS), "filter_mode": settings.filter_mode}
