"""Local development entry — use a WSGI server (e.g. Gunicorn + eventlet) in production."""

import os

from app import create_app
from app.extensions import socketio

config_name = os.environ.get("FLASK_CONFIG", "development")
app = create_app(config_name)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    socketio.run(app, host=host, port=port, debug=app.debug, use_reloader=app.debug)
