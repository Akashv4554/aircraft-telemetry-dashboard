from flask import Blueprint, jsonify

from app.models.aircraft import Aircraft
from app.models.telemetry import Telemetry

dashboard_bp = Blueprint(
    "dashboard_routes",
    __name__,
    url_prefix="/api/dashboard",
)


@dashboard_bp.route("/summary", methods=["GET"])
def dashboard_summary():

    total_aircraft = Aircraft.query.count()

    online_aircraft = Aircraft.query.filter_by(
        status="ONLINE"
    ).count()

    offline_aircraft = Aircraft.query.filter_by(
        status="OFFLINE"
    ).count()

    latest_telemetry = (
        Telemetry.query.order_by(
            Telemetry.timestamp.desc()
        ).limit(10).all()
    )

    return jsonify({
        "total_aircraft": total_aircraft,
        "online_aircraft": online_aircraft,
        "offline_aircraft": offline_aircraft,
        "latest_telemetry": [
            telemetry.to_dict()
            for telemetry in latest_telemetry
        ],
    })