"""Standardized JSON API responses."""

from __future__ import annotations

from typing import Any

from flask import jsonify

from app.models.user import User


def success_response(
    message: str,
    *,
    data: dict[str, Any] | None = None,
    status_code: int = 200,
):
    payload: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
        "errors": [],
    }
    return jsonify(payload), status_code


def error_response(
    message: str,
    *,
    errors: list[dict[str, str]] | None = None,
    data: dict[str, Any] | None = None,
    status_code: int = 400,
):
    payload: dict[str, Any] = {
        "success": False,
        "message": message,
        "data": data if data is not None else {},
        "errors": errors or [],
    }
    return jsonify(payload), status_code


def public_user(user: User) -> dict[str, Any]:
    """Serialize user for API output — never includes password hash."""
    return {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


def marshmallow_to_error_list(messages: dict[str, Any]) -> list[dict[str, str]]:
    """Flatten Marshmallow validation messages into `{field, message}` entries."""

    out: list[dict[str, str]] = []

    def walk(prefix: str, node: Any) -> None:
        if isinstance(node, dict):
            for key, val in node.items():
                path = f"{prefix}.{key}" if prefix else key
                walk(path, val)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, dict):
                    walk(prefix, item)
                else:
                    out.append({"field": prefix or "body", "message": str(item)})
        else:
            out.append({"field": prefix or "body", "message": str(node)})

    walk("", messages)
    return out
