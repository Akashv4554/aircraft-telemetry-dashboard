"""Local development entry — use a WSGI server (e.g. Gunicorn + eventlet) in production."""

import os

from app import create_app
from app.extensions import socketio

config_name = os.getenv("FLASK_CONFIG", "development")

app = create_app(config_name)

if __name__ == "__main__":
    socketio.run(
    app,
    host=app.config.get("HOST", "0.0.0.0"),
    port=int(app.config.get("PORT", 5000)),
    debug=True,
)