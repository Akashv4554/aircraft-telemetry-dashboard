from flask import Blueprint, jsonify

from app.models.alert import Alert

alert_bp = Blueprint(
    "alert_routes",
    __name__,
    url_prefix="/api/alerts",
)


@alert_bp.route("", methods=["GET"])
def get_alerts():

    alerts = (
        Alert.query.order_by(
            Alert.created_at.desc()
        ).all()
    )

    return jsonify({
        "count": len(alerts),
        "alerts": [
            alert.to_dict()
            for alert in alerts
        ],
    })