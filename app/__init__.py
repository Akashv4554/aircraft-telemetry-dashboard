"""Application package — Flask app factory."""

import os

from flask import Flask, app, request

from app.config import CONFIG_MAP
from app.extensions import db, jwt, migrate, redis_ext, socketio
from app.middleware.errors import register_error_handlers
from app.utils.logging import configure_logging


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    resolved = config_name or os.environ.get("FLASK_CONFIG", "development")
    if resolved not in CONFIG_MAP:
        resolved = "development"
    app.config.from_object(CONFIG_MAP[resolved])
    if resolved == "production" and not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise ValueError("DATABASE_URL must be set when FLASK_CONFIG=production")

    configure_logging(app)
    _init_extensions(app)
    _register_request_logging(app)
    register_blueprints(app)
    register_error_handlers(app)
    _register_socketio_handlers()
    from app.routes.aircraft_routes import aircraft_bp
    app.register_blueprint(aircraft_bp)
    from app.routes.telemetry_routes import telemetry_bp
    app.register_blueprint(telemetry_bp)
    from app import socket_events
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    @app.shell_context_processor
    def shell_context():
        from app import models  # noqa: F401

        return {"db": db}
    
    return app


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    redis_ext.init_app(app)

    message_queue = app.config.get("SOCKETIO_MESSAGE_QUEUE")
    socketio.init_app(
        app,
        cors_allowed_origins=app.config.get("SOCKETIO_CORS_ORIGINS", "*"),
        async_mode=app.config.get("SOCKETIO_ASYNC_MODE", "threading"),
        message_queue=message_queue,
        logger=app.debug,
        engineio_logger=app.debug,
    )


def _register_socketio_handlers() -> None:
    # Import for side effects — registers Socket.IO event handlers on `socketio`.
    from app.socketio_handlers import events  # noqa: F401


def _register_request_logging(app: Flask) -> None:
    @app.before_request
    def log_api_request():
        if not request.path.startswith("/api"):
            return
        app.logger.info("%s %s", request.method, request.path)


def register_blueprints(app: Flask) -> None:
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.health import bp as health_bp
    from app.blueprints.telemetry import bp as telemetry_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(telemetry_bp, url_prefix="/api/telemetry")
