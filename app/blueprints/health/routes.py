"""Liveness and readiness endpoints."""

from __future__ import annotations

import logging

from flask import Blueprint, jsonify

from sqlalchemy import text

from app.extensions import db, redis_ext

logger = logging.getLogger(__name__)

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@bp.get("/ready")
def ready():
    checks: dict[str, str] = {}
    status = "ready"

    try:
        db.session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:  # noqa: BLE001
        logger.exception("Readiness database check failed")
        checks["database"] = f"error: {exc}"
        status = "not_ready"

    if redis_ext.client is not None:
        checks["redis"] = "ok" if redis_ext.ping() else "error: ping failed"
        if checks["redis"] != "ok":
            status = "not_ready"

    code = 200 if status == "ready" else 503
    return jsonify({"status": status, "checks": checks}), code
