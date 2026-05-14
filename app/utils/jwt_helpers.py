"""JWT creation helpers — keeps token claims consistent across auth flows."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from uuid import UUID

from flask import current_app, g
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity

from app.repositories.user_repository import UserRepository

if TYPE_CHECKING:
    from app.models.user import User

logger = logging.getLogger(__name__)


def _access_expires_seconds() -> int:
    delta = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    return int(delta.total_seconds())


def additional_claims_for_user(user: User) -> dict[str, Any]:
    return {
        "email": user.email,
        "username": user.username,
    }


def issue_token_pair(user: User) -> dict[str, Any]:
    """Return access + refresh tokens and metadata for API responses."""
    identity = str(user.id)
    claims = additional_claims_for_user(user)
    access = create_access_token(identity=identity, additional_claims=claims)
    refresh = create_refresh_token(identity=identity)
    payload = {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "Bearer",
        "expires_in": _access_expires_seconds(),
    }
    logger.debug("Issued JWT pair for user_id=%s", identity)
    return payload


def issue_access_token(user: User) -> dict[str, Any]:
    """Issue a new access token (e.g. after refresh)."""
    identity = str(user.id)
    claims = additional_claims_for_user(user)
    access = create_access_token(identity=identity, additional_claims=claims)
    return {
        "access_token": access,
        "token_type": "Bearer",
        "expires_in": _access_expires_seconds(),
    }


def parse_uuid_identity(identity: str | None) -> UUID | None:
    if not identity:
        return None
    try:
        return UUID(str(identity))
    except (ValueError, TypeError, AttributeError):
        return None


_USER_SENTINEL = object()


def get_current_user() -> User | None:
    """Resolve the authenticated user from the JWT identity (cached per request on `g`)."""
    cached = getattr(g, "_jwt_current_user", _USER_SENTINEL)
    if cached is not _USER_SENTINEL:
        return cached  # type: ignore[return-value]

    uid = parse_uuid_identity(get_jwt_identity())
    if uid is None:
        g._jwt_current_user = None
        return None
    user = UserRepository().get_by_id(uid)
    g._jwt_current_user = user
    return user
