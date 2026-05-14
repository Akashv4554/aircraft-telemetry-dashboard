"""User persistence — keeps SQLAlchemy access out of services."""

from __future__ import annotations

import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.extensions import db
from app.models.user import User

logger = logging.getLogger(__name__)


class UserRepository:
    """Data access for `User` records."""

    def __init__(self, session: Session | None = None) -> None:
        self._session = session or db.session

    def get_by_id(self, user_id: UUID) -> User | None:
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        return self._session.scalars(stmt).first()

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username).limit(1)
        return self._session.scalars(stmt).first()

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def username_exists(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def create(
        self,
        *,
        email: str,
        username: str,
        password_hash: str,
    ) -> User:
        user = User(email=email, username=username, password_hash=password_hash)
        self._session.add(user)
        self._session.commit()
        logger.info("User persisted id=%s email=%s", user.id, email)
        return user
