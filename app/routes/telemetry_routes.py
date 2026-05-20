from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.aircraft import Aircraft
from app.models.telemetry import Telemetry

telemetry_bp = Blueprint(
    "telemetry_routes",
    __name__,
    url_prefix="/api/telemetry",
)


@telemetry_bp.route("", methods=["POST"])
def create_telemetry():
    """
    Create a telemetry record for an aircraft.
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "aircraft_id",
        "latitude",
        "longitude",
        "altitude",
        "speed",
        "heading",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    aircraft = Aircraft.query.get(data["aircraft_id"])

    if not aircraft:
        return jsonify({"error": "Aircraft not found"}), 404

    telemetry = Telemetry(
        aircraft_id=data["aircraft_id"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        altitude=data["altitude"],
        speed=data["speed"],
        heading=data["heading"],
        vertical_speed=data.get("vertical_speed"),
        fuel_level=data.get("fuel_level"),
        engine_temperature=data.get("engine_temperature"),
        outside_temperature=data.get("outside_temperature"),
        pressure=data.get("pressure"),
    )

    db.session.add(telemetry)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Telemetry record created successfully",
                "telemetry": telemetry.to_dict(),
            }
        ),
        201,
    )


@telemetry_bp.route("/latest/<int:aircraft_id>", methods=["GET"])
def get_latest_telemetry(aircraft_id):
    """
    Get latest telemetry record for an aircraft.
    """

    aircraft = Aircraft.query.get(aircraft_id)

    if not aircraft:
        return jsonify({"error": "Aircraft not found"}), 404

    telemetry = (
        Telemetry.query.filter_by(aircraft_id=aircraft_id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

    if not telemetry:
        return jsonify({"error": "No telemetry data found"}), 404

    return jsonify(telemetry.to_dict()), 200


@telemetry_bp.route("/history/<int:aircraft_id>", methods=["GET"])
def get_telemetry_history(aircraft_id):
    """
    Get telemetry history for an aircraft.
    """

    aircraft = Aircraft.query.get(aircraft_id)

    if not aircraft:
        return jsonify({"error": "Aircraft not found"}), 404

    telemetry_records = (
        Telemetry.query.filter_by(aircraft_id=aircraft_id)
        .order_by(Telemetry.timestamp.desc())
        .all()
    )

    return (
        jsonify(
            {
                "aircraft_id": aircraft_id,
                "count": len(telemetry_records),
                "telemetry": [
                    telemetry.to_dict()
                    for telemetry in telemetry_records
                ],
            }
        ),
        200,
    )