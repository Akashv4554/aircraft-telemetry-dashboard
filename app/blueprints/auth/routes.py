"""Authentication API — register, login, profile, refresh."""

from __future__ import annotations

import logging

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.blueprints.auth.decorators import jwt_user_required
from app.schemas.auth_schema import LoginSchema, RegisterSchema
from app.services import auth_service
from app.utils.jwt_helpers import get_current_user, issue_token_pair
from app.utils.responses import public_user, success_response

logger = logging.getLogger(__name__)

bp = Blueprint("auth", __name__)

_login_schema = LoginSchema()
_register_schema = RegisterSchema()


@bp.post("/register")
def register():
    payload = _register_schema.load(request.get_json(silent=True) or {})
    user = auth_service.register_user(
        email=payload["email"],
        username=payload["username"],
        password=payload["password"],
    )
    tokens = issue_token_pair(user)
    logger.info("API register success user_id=%s", user.id)
    return success_response(
        "Registration successful.",
        data={"user": public_user(user), "tokens": tokens},
        status_code=201,
    )


@bp.post("/login")
def login():
    payload = _login_schema.load(request.get_json(silent=True) or {})
    user = auth_service.authenticate_user(
        email=payload["email"],
        password=payload["password"],
    )
    tokens = issue_token_pair(user)
    logger.info("API login success user_id=%s", user.id)
    return success_response(
        "Login successful.",
        data={"user": public_user(user), "tokens": tokens},
    )


@bp.get("/profile")
@jwt_user_required
def profile():
    user = get_current_user()
    assert user is not None
    logger.info("API profile user_id=%s", user.id)
    return success_response(
        "Profile retrieved.",
        data={"user": public_user(user)},
    )


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    tokens = auth_service.refresh_session(get_jwt_identity())
    logger.info("API refresh success")
    return success_response(
        "Token refreshed.",
        data={"tokens": tokens},
    )
