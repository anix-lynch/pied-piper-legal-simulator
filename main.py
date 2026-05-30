"""
VC Term-Sheet Advisor — Cloud Run entrypoint.

Serves the grounded advisor UI at / and the JSON endpoint at /api/advise.
Same grounded-RAG pattern as the healthcare service, retargeted to the
clause + Silicon Valley corpus. Runtime auth = Cloud Run service identity
(bchan-genai-deploy@, has Vertex AI User) so Gemini grounding works in prod.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from advisor import advise

BASE = Path(__file__).resolve().parent
WEB = BASE / "web"

app = FastAPI(title="VC Term-Sheet Advisor", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def home():
    idx = WEB / "index.html"
    if not idx.exists():
        raise HTTPException(404, "UI not built")
    return FileResponse(idx)


@app.get("/api/advise")
def api_advise(q: str = Query(..., min_length=2, description="A term-sheet clause or term")):
    return advise(q)


@app.get("/healthz")
def healthz():
    return {"ok": True}
