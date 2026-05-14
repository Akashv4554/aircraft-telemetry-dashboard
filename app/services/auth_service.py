"""Authentication use-cases — orchestrates repositories and crypto."""

from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.exceptions import AuthError
from app.extensions import db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils import jwt_helpers
from app.utils.password import hash_password, verify_password

logger = logging.getLogger(__name__)


def register_user(*, email: str, username: str, password: str) -> User:
    repo = UserRepository()
    if repo.email_exists(email):
        raise AuthError(
            "Registration could not be completed.",
            status_code=409,
            errors=[
                {
                    "field": "email",
                    "message": "An account with this email already exists.",
                }
            ],
        )
    if repo.username_exists(username):
        raise AuthError(
            "Registration could not be completed.",
            status_code=409,
            errors=[
                {
                    "field": "username",
                    "message": "This username is already taken.",
                }
            ],
        )
    try:
        user = repo.create(
            email=email,
            username=username,
            password_hash=hash_password(password),
        )
    except IntegrityError:
        db.session.rollback()
        logger.warning("IntegrityError during user registration (race on unique field)")
        raise AuthError(
            "Registration could not be completed.",
            status_code=409,
            errors=[
                {
                    "field": "email",
                    "message": "An account with this email or username already exists.",
                }
            ],
        ) from None
    logger.info("Registered user id=%s username=%s", user.id, username)
    return user


def authenticate_user(email: str, password: str) -> User:
    repo = UserRepository()
    user = repo.get_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        logger.info("Failed login attempt for email=%s", email)
        raise AuthError(
            "Invalid email or password.",
            status_code=401,
        )
    logger.info("Successful login id=%s", user.id)
    return user


def get_user_profile(user_id: UUID) -> User:
    repo = UserRepository()
    user = repo.get_by_id(user_id)
    if user is None:
        raise AuthError("User not found.", status_code=404)
    return user


def refresh_session(identity: str | None) -> dict:
    """Build a new access token payload for a refresh JWT subject."""
    uid = jwt_helpers.parse_uuid_identity(identity)
    if uid is None:
        raise AuthError("Invalid or expired token.", status_code=401)
    user = UserRepository().get_by_id(uid)
    if user is None:
        raise AuthError("Invalid or expired token.", status_code=401)
    logger.debug("Refresh issued for user_id=%s", uid)
    return jwt_helpers.issue_access_token(user)
