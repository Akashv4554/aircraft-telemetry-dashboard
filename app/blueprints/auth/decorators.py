"""Blueprint-level auth decorators."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from flask_jwt_extended import jwt_required

from app.utils.jwt_helpers import get_current_user
from app.utils.responses import error_response

F = TypeVar("F", bound=Callable[..., Any])


def jwt_user_required(view: F) -> F:
    """Require a valid JWT whose subject resolves to an existing user."""

    @wraps(view)
    @jwt_required()
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        user = get_current_user()
        if user is None:
            return error_response(
                "Invalid or expired token.",
                status_code=401,
            )
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
