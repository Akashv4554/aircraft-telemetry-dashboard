from datetime import datetime, UTC

from app.extensions import db


class Telemetry(db.Model):
    """
    Telemetry model storing real-time aircraft telemetry data.
    """

    __tablename__ = "telemetry"

    id = db.Column(db.Integer, primary_key=True)

    aircraft_id = db.Column(
        db.Integer,
        db.ForeignKey("aircraft.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    latitude = db.Column(
        db.Float,
        nullable=False,
    )

    longitude = db.Column(
        db.Float,
        nullable=False,
    )

    altitude = db.Column(
        db.Float,
        nullable=False,
    )

    speed = db.Column(
        db.Float,
        nullable=False,
    )

    heading = db.Column(
        db.Float,
        nullable=False,
    )

    vertical_speed = db.Column(
        db.Float,
        nullable=True,
    )

    fuel_level = db.Column(
        db.Float,
        nullable=True,
    )

    engine_temperature = db.Column(
        db.Float,
        nullable=True,
    )

    outside_temperature = db.Column(
        db.Float,
        nullable=True,
    )

    pressure = db.Column(
        db.Float,
        nullable=True,
    )

    timestamp = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    # Relationship:
    # Each telemetry record belongs to one aircraft
    aircraft = db.relationship(
        "Aircraft",
        back_populates="telemetry_records",
    )

    def to_dict(self) -> dict:
        """
        Convert telemetry object to dictionary.
        """

        return {
            "id": self.id,
            "aircraft_id": self.aircraft_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "speed": self.speed,
            "heading": self.heading,
            "vertical_speed": self.vertical_speed,
            "fuel_level": self.fuel_level,
            "engine_temperature": self.engine_temperature,
            "outside_temperature": self.outside_temperature,
            "pressure": self.pressure,
            "timestamp": (
                self.timestamp.isoformat()
                if self.timestamp
                else None
            ),
        }

    def __repr__(self) -> str:
        return (
            f"<Telemetry "
            f"id={self.id} "
            f"aircraft_id={self.aircraft_id} "
            f"altitude={self.altitude} "
            f"speed={self.speed}>"
        )