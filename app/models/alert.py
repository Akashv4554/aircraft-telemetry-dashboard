from datetime import datetime, UTC

from app.extensions import db


class Alert(db.Model):

    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)

    aircraft_id = db.Column(
        db.Integer,
        db.ForeignKey("aircraft.id", ondelete="CASCADE"),
        nullable=False,
    )

    alert_type = db.Column(
        db.String(100),
        nullable=False,
    )

    severity = db.Column(
        db.String(20),
        nullable=False,
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    is_resolved = db.Column(
        db.Boolean,
        default=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    aircraft = db.relationship(
        "Aircraft",
        backref="alerts",
    )

    def to_dict(self):

        return {
            "id": self.id,
            "aircraft_id": self.aircraft_id,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "is_resolved": self.is_resolved,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }