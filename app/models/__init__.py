"""SQLAlchemy models — import here so Flask-Migrate discovers metadata."""

from app.models.user import User

__all__ = ["User"]
