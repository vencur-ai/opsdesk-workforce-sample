"""3.1.5 (B2): what a delivery's own scorer returns, per licence.

- **Training licence**: the delivery ships its requests' solver references, sealed into the scoring image (the
  separate Harbor verifier, the HUD container, the OpenEnv/HTTP server). Every format returns the deterministic
  score as a number and `passed`. The agent's container and the app image carry no reference.
- **Evaluation licence**: no reference leaves the provider. Every format still finishes with a number – a placeholder
  `0.0` with `passed: false` and `scored: false` – and keeps the workspace record; Vencur scores the returned records.
  The placeholder is never a result.

`finish(ws)` is the one place the app, the HUD template and the Harbor verifier ask for the end-of-run outcome; with
a reference it is exactly `WorkforceSession.finish()` (verifier unchanged).
"""

from __future__ import annotations

from typing import Any

LICENCES = ("evaluation", "training")
ALIASES = {"eval": "evaluation"}
SAMPLE_WORDS = ("sample", "muster", "public", "demo")  # as `opsdesk motor pack`
PENDING = "pending_provider_scoring"
PLACEHOLDER_NOTE = ("Evaluation licence: the solver references stay with the provider, so this run is not scored here. "
                    "0.0 is a placeholder, not a result; Vencur scores the kept workspace record.")


class LicenceError(ValueError):
    pass


def normalise(licence: str) -> str:
    name = ALIASES.get(licence, licence)
    if name not in LICENCES:
        raise LicenceError(f"unknown licence {licence!r}; use training or eval")
    return name


def check(licence: str, label: str) -> bool:
    """Validate a delivery's licence; True when it ships references (training only). `label` is the buyer and
    delivery name: a sample, public or demo delivery never ships references."""
    name = normalise(licence)
    if name == "training" and any(w in label.lower() for w in SAMPLE_WORDS):  # fail closed, as `motor pack`
        raise LicenceError("samples, public and demo deliveries never ship references; use --licence eval")
    return name == "training"


def has_reference(ws: Any) -> bool:
    from opsdesk.verifiers.score import _load_reference
    try:
        _load_reference(ws.task_dir, ws.task["task_id"])
    except FileNotFoundError:
        return False
    return True


def finish(ws: Any) -> dict[str, Any]:
    """End the run. With the request's reference: the verifier's result plus `scored: true`. Without (evaluation
    licence): the workspace is locked as `finish()` would lock it, nothing is scored, and the outcome says so."""
    if has_reference(ws):
        result = ws.finish()
        return {**result, "score": {**result["score"], "scored": True}, "status": "scored"}
    ws.locked = True
    return {"score": {"total_score": 0.0, "passed": False, "scored": False}, "status": PENDING,
            "note": PLACEHOLDER_NOTE, "state_hash": ws.state_hash()}


def hud_frame(result: dict[str, Any]) -> dict[str, Any]:
    """HUD's grade frame: a numeric `score`, and `passed`/`scored` in `info` (HUD's metadata field)."""
    score = result["score"]
    frame = {"score": float(score["total_score"]), "done": True,
             "info": {"passed": bool(score["passed"]), "scored": bool(score["scored"]), "status": result["status"]}}
    if not score["scored"]:
        frame["content"] = PLACEHOLDER_NOTE
    return frame
