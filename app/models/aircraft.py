from datetime import datetime, UTC

from app.extensions import db


class Aircraft(db.Model):
    """
    Aircraft model representing a tracked aircraft in the telemetry system.
    """

    __tablename__ = "aircraft"

    id = db.Column(db.Integer, primary_key=True)

    callsign = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    aircraft_type = db.Column(
        db.String(50),
        nullable=False,
    )

    airline = db.Column(
        db.String(100),
        nullable=True,
    )

    manufacturer = db.Column(
        db.String(100),
        nullable=True,
    )

    capacity = db.Column(
        db.Integer,
        nullable=True,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVE",
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationship:
    # One aircraft can have many telemetry records
    telemetry_records = db.relationship(
        "Telemetry",
        back_populates="aircraft",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def to_dict(self) -> dict:
        """
        Convert aircraft object to dictionary.
        """

        return {
            "id": self.id,
            "callsign": self.callsign,
            "aircraft_type": self.aircraft_type,
            "airline": self.airline,
            "manufacturer": self.manufacturer,
            "capacity": self.capacity,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            ),
        }

    def __repr__(self) -> str:
        return (
            f"<Aircraft "
            f"id={self.id} "
            f"callsign={self.callsign} "
            f"type={self.aircraft_type}>"
        )