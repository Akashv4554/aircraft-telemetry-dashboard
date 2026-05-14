"""Application-wide domain exceptions."""


class AuthError(Exception):
    """Raised when authentication or registration rules are violated."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        errors: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
