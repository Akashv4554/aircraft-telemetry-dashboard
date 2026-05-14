"""Telemetry API — extend with aircraft channels, ingestion, and history queries."""

from __future__ import annotations

import logging

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

logger = logging.getLogger(__name__)

bp = Blueprint("telemetry", __name__)


@bp.get("/stream-status")
@jwt_required()
def stream_status():
    """Placeholder for ingestion / websocket coordination."""
    logger.info("Telemetry stream-status requested")
    return jsonify({"ingestion": "idle", "last_frame_ms": None}), 200
