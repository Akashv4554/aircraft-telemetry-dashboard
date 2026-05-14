"""Auth request validation — composes Marshmallow with shared validators."""

from __future__ import annotations

from marshmallow import Schema, fields, post_load, validates

from app.validators.auth_validators import (
    normalize_email,
    normalize_username,
    validate_password_strength,
    validate_username_format,
)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @validates("username")
    def validate_username(self, value: str) -> None:
        validate_username_format(value)

    @validates("password")
    def validate_password(self, value: str) -> None:
        validate_password_strength(value)

    @post_load
    def normalize_identity(self, data: dict, **_kwargs) -> dict:
        data["email"] = normalize_email(data["email"])
        data["username"] = normalize_username(data["username"])
        return data


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

    @post_load
    def normalize_email_field(self, data: dict, **_kwargs) -> dict:
        data["email"] = normalize_email(data["email"])
        return data
