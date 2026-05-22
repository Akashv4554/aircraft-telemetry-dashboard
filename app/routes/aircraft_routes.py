from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.aircraft import Aircraft

aircraft_bp = Blueprint("aircraft_routes", __name__, url_prefix="/api/aircraft")


@aircraft_bp.route("", methods=["POST"])
def create_aircraft():
    """
    Create a new aircraft.
    """

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["callsign", "aircraft_type"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    existing_aircraft = Aircraft.query.filter_by(
        callsign=data["callsign"]
    ).first()

    if existing_aircraft:
        return jsonify({"error": "Callsign already exists"}), 409

    aircraft = Aircraft(
        callsign=data["callsign"],
        aircraft_type=data["aircraft_type"],
        airline=data.get("airline"),
        manufacturer=data.get("manufacturer"),
        capacity=data.get("capacity"),
        status=data.get("status", "ACTIVE"),
    )

    db.session.add(aircraft)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Aircraft created successfully",
                "aircraft": aircraft.to_dict(),
            }
        ),
        201,
    )


@aircraft_bp.route("", methods=["GET"])
def get_all_aircraft():
    """
    Get all aircraft.
    """

    aircraft_list = Aircraft.query.order_by(Aircraft.id.asc()).all()

    return (
        jsonify(
            {
                "count": len(aircraft_list),
                "aircraft": [
                    aircraft.to_dict()
                    for aircraft in aircraft_list
                ],
            }
        ),
        200,
    )


@aircraft_bp.route("/<int:aircraft_id>", methods=["GET"])
def get_aircraft(aircraft_id):
    """
    Get aircraft by ID.
    """

    aircraft = Aircraft.query.get(aircraft_id)

    if not aircraft:
        return jsonify({"error": "Aircraft not found"}), 404

    return jsonify(aircraft.to_dict()), 200


@aircraft_bp.route("/<int:aircraft_id>", methods=["DELETE"])
def delete_aircraft(aircraft_id):
    """
    Delete aircraft by ID.
    """

    aircraft = Aircraft.query.get(aircraft_id)

    if not aircraft:
        return jsonify({"error": "Aircraft not found"}), 404

    db.session.delete(aircraft)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Aircraft deleted successfully",
                "aircraft_id": aircraft_id,
            }
        ),
        200,
    )
