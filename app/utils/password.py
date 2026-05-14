"""Bcrypt password hashing and verification."""

from __future__ import annotations

import logging

import bcrypt

logger = logging.getLogger(__name__)


def _rounds() -> int:
    try:
        from flask import current_app

        raw = current_app.config.get("BCRYPT_ROUNDS", 12)
        return int(raw)
    except RuntimeError:
        return 12


def hash_password(plain_password: str, *, rounds: int | None = None) -> str:
    """Hash a plaintext password using bcrypt."""
    cost = rounds if rounds is not None else _rounds()
    if cost < 10 or cost > 31:
        logger.warning("BCRYPT_ROUNDS out of range; clamping to 12")
        cost = 12
    salt = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Constant-time verification against a stored bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False
