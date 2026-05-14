"""Application logging configuration."""

from __future__ import annotations

import logging
import sys
from logging.config import dictConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask


def configure_logging(app: Flask) -> None:
    level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    fmt = app.config.get(
        "LOG_FORMAT",
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": fmt,
                    "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "default",
                    "level": level,
                },
            },
            "root": {"handlers": ["console"], "level": level},
            "loggers": {
                "werkzeug": {"level": level, "propagate": True},
                "sqlalchemy.engine": {
                    "level": logging.WARNING,
                    "propagate": True,
                },
            },
        }
    )

    # Flask attaches its own handler; route everything through the root config above.
    app.logger.handlers.clear()
    app.logger.propagate = True
    app.logger.setLevel(level)
    app.logger.info("Logging configured at %s", logging.getLevelName(level))
