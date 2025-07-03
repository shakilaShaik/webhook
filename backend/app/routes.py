from flask import Blueprint, request, jsonify
from .db import db
from .models import GitHubEvent, build_event_from_github_payload

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET"])
def root():
    return "✅ Webhook backend is live", 200


@routes.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    event_type = request.headers.get("X-GitHub-Event")

    event = build_event_from_github_payload(event_type, data)

    if event:
        db.events.insert_one(event.dict())  # Pydantic model to dict
        return jsonify({"status": "saved"}), 200
    return jsonify({"status": "ignored"}), 200


@routes.route("/events", methods=["GET"])
def get_events():
    events = list(db.events.find().sort("_id", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)
