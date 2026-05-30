"""
VC Term-Sheet Advisor — grounded on the clause library + Silicon Valley episodes.

Same grounded-RAG pattern as the healthcare /api/ask service, retargeted to the
legal/VC domain: retrieve the most relevant clause(s) from data/clauses.json,
pull the matching Silicon Valley episode (linked by conflict_type), then ground a
Gemini answer ONLY on that evidence with a [clause_id] citation. No fund math —
this is the read-a-term-and-instantly-understand-it layer.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

DATA = Path(__file__).resolve().parent / "data"
_PROJECT = os.environ.get("GCP_PROJECT_ID", "bchan-genai-lab")
_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
_MODEL = os.environ.get("ADVISOR_MODEL", "gemini-2.5-flash")

_CLAUSES = json.loads((DATA / "clauses.json").read_text())
_EPISODES = json.loads((DATA / "episodes.json").read_text())
_TOKEN = re.compile(r"[a-z0-9]+")


def _toks(s: str) -> set[str]:
    return set(_TOKEN.findall((s or "").lower()))


def _retrieve(query: str, k: int = 3) -> list[dict[str, Any]]:
    q = _toks(query)
    scored = []
    for c in _CLAUSES:
        hay = _toks(" ".join([
            c.get("short_text", ""), c.get("full_text", ""),
            c.get("clause_type", ""), c.get("conflict_type", ""),
            c.get("explanation", ""),
        ]))
        scored.append((len(q & hay), c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:k] if s > 0] or [scored[0][1]]


def _episode_for(conflict_type: str) -> dict[str, Any] | None:
    for e in _EPISODES:
        if e.get("conflict_type") == conflict_type:
            return e
    return None


def advise(query: str) -> dict[str, Any]:
    hits = _retrieve(query)
    top = hits[0]
    ep = _episode_for(top.get("conflict_type", ""))

    ctx_clauses = "\n".join(
        f"[{c['clause_id']}] {c['clause_type']} ({c['bias']}) — {c['short_text']}. "
        f"{c['explanation']} (founder_risk={c['risk_score_founder']}, vc_risk={c['risk_score_vc']})"
        for c in hits
    )
    ep_ctx = (
        f"{ep['episode_id']} '{ep['title']}': {ep['scene']} → {ep['result']} "
        f"(stakes: {ep['legal_stakes']})" if ep else "no matching episode"
    )

    sources = [{
        "clause_id": c["clause_id"], "clause_type": c["clause_type"],
        "bias": c["bias"], "risk_score_founder": c["risk_score_founder"],
        "risk_score_vc": c["risk_score_vc"],
    } for c in hits]

    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel, GenerationConfig

        vertexai.init(project=_PROJECT, location=_LOCATION)
        prompt = (
            "You are a VC term-sheet advisor for a new analyst. Answer ONLY from the "
            "clause evidence and the Silicon Valley episode below. Cite [clause_id]. "
            "Cover, in 3-4 sentences: (1) plain-English meaning, (2) who it favors and "
            "the founder/VC risk scores, (3) the DIRECTION it pushes fund returns "
            "(favorable/unfavorable to the VC — qualitative, no math), (4) the matching "
            "Silicon Valley moment.\n\n"
            f"Clause evidence:\n{ctx_clauses}\n\nSilicon Valley episode:\n{ep_ctx}\n\n"
            f"Question: {query}\nAnswer:"
        )
        model = GenerativeModel(_MODEL)
        resp = model.generate_content(
            prompt, generation_config=GenerationConfig(temperature=0.2, max_output_tokens=2048)
        )
        answer, grounded = (resp.text or "").strip(), True
    except Exception as exc:
        answer = f"Retrieval ran (sources below); grounded generation unavailable: {type(exc).__name__}"
        grounded = False

    return {
        "query": query,
        "grounded": grounded,
        "model": _MODEL,
        "answer": answer,
        "top_clause": top["clause_id"],
        "founder_risk": top["risk_score_founder"],
        "vc_risk": top["risk_score_vc"],
        "bias": top["bias"],
        "episode": (f"{ep['episode_id']} — {ep['title']}" if ep else None),
        "sources": sources,
        "corpus": "57 clauses + 19 Silicon Valley episodes",
    }


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "2x participating liquidation preference"
    out = advise(q)
    print(json.dumps(out, indent=2))
