"""SQLAlchemy models — import here so Flask-Migrate discovers metadata."""

from app.models.user import User
from app.models.aircraft import Aircraft
from app.models.telemetry import Telemetry

__all__ = ["User"]
