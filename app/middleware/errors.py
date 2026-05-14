"""Centralized JSON error responses and logging."""

from __future__ import annotations

import logging
import traceback
from http import HTTPStatus
from typing import Any

from flask import Flask, request
from flask_jwt_extended.exceptions import JWTExtendedException
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from app.exceptions import AuthError
from app.utils.responses import error_response, marshmallow_to_error_list

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AuthError)
    def handle_auth_error(exc: AuthError):
        _log_request_context("info", exc)
        return error_response(
            exc.message,
            errors=exc.errors,
            status_code=exc.status_code,
        )

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_extended(exc: JWTExtendedException):
        _log_request_context("warning", exc)
        code = getattr(exc, "code", 401) or 401
        return error_response(
            "Invalid or expired token.",
            status_code=int(code),
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        _log_request_context("warning", exc)
        message = exc.description if isinstance(exc.description, str) else exc.name
        return error_response(
            message or exc.name,
            status_code=exc.code or HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        _log_request_context("info", exc)
        errors = marshmallow_to_error_list(exc.messages)
        return error_response(
            "Validation failed.",
            errors=errors,
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(exc: SQLAlchemyError):
        logger.exception("Database error: %s", exc)
        return error_response(
            "A database error occurred.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        logger.exception("Unhandled error: %s\n%s", exc, traceback.format_exc())
        return error_response(
            "An unexpected error occurred.",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


def _log_request_context(level: str, exc: BaseException) -> None:
    log = getattr(logger, level, logger.warning)
    log(
        "%s %s - %s: %s",
        request.method,
        request.path,
        type(exc).__name__,
        exc,
    )
