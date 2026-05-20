"""Flask extensions — instantiated here, bound in app factory."""

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.utils.redis_client import RedisExtension

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="threading",
)
redis_ext = RedisExtension()
