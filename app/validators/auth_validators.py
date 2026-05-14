"""Field-level validation rules for authentication payloads."""

from __future__ import annotations

import re

from marshmallow import ValidationError

# 3-32 chars, start with letter, then letters, digits, underscore
USERNAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{2,31}$")

_PASSWORD_UPPER = re.compile(r"[A-Z]")
_PASSWORD_LOWER = re.compile(r"[a-z]")
_PASSWORD_DIGIT = re.compile(r"\d")
_PASSWORD_SPECIAL = re.compile(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]")
_PASSWORD_SPACE = re.compile(r"\s")


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_username(value: str) -> str:
    return value.strip().lower()


def validate_username_format(value: str) -> str:
    if not value or not isinstance(value, str):
        raise ValidationError("Username is required.")
    candidate = normalize_username(value)
    if not USERNAME_PATTERN.match(candidate):
        raise ValidationError(
            "Username must be 3-32 characters, start with a letter, "
            "and contain only letters, digits, and underscores."
        )
    return candidate


def validate_password_strength(value: str) -> str:
    if not value or not isinstance(value, str):
        raise ValidationError("Password is required.")
    if len(value) < 12 or len(value) > 128:
        raise ValidationError("Password must be between 12 and 128 characters.")
    if _PASSWORD_SPACE.search(value):
        raise ValidationError("Password must not contain spaces.")
    if not _PASSWORD_UPPER.search(value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not _PASSWORD_LOWER.search(value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not _PASSWORD_DIGIT.search(value):
        raise ValidationError("Password must contain at least one digit.")
    if not _PASSWORD_SPECIAL.search(value):
        raise ValidationError(
            "Password must contain at least one special character "
            "(e.g. !@#$%^&*)."
        )
    return value
