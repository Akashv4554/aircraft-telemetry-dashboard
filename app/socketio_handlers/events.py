"""Realtime channel — wire dashboard subscriptions to your telemetry bus."""

from __future__ import annotations

import logging

from flask import request
from flask_jwt_extended import decode_token
from flask_socketio import ConnectionRefusedError, join_room

from app.extensions import socketio

logger = logging.getLogger(__name__)


def _token_from_auth(auth: dict | None) -> str | None:
    if not auth or not isinstance(auth, dict):
        return None
    return auth.get("token")


@socketio.on("connect")
def handle_connect(auth):
    token = _token_from_auth(auth)
    if not token:
        logger.warning("Socket connect rejected — missing token")
        raise ConnectionRefusedError("unauthorized")
    try:
        decoded = decode_token(token)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Socket connect rejected — invalid token: %s", exc)
        raise ConnectionRefusedError("unauthorized") from exc
    user_id = decoded.get("sub")
    if not user_id:
        raise ConnectionRefusedError("unauthorized")
    join_room(f"user:{user_id}")
    logger.info("Socket connected sid=%s user=%s", request.sid, user_id)


@socketio.on("disconnect")
def handle_disconnect():
    logger.info("Socket disconnected sid=%s", request.sid)


@socketio.on("telemetry_subscribe")
def handle_telemetry_subscribe(data):
    """Client requests a feed — validate aircraft id and join room."""
    aircraft_id = (data or {}).get("aircraft_id")
    if not aircraft_id:
        return {"ok": False, "error": "aircraft_id required"}
    join_room(f"aircraft:{aircraft_id}")
    logger.info("sid=%s subscribed to aircraft:%s", request.sid, aircraft_id)
    return {"ok": True, "room": f"aircraft:{aircraft_id}"}
