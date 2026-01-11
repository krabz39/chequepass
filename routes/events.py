from flask import Blueprint, request, jsonify, session
import uuid
from db import query

events = Blueprint("events", __name__)

@events.get("/events")
def list_events():
    rows = query("SELECT id,title,venue,city,start_time FROM events WHERE status='live'", fetchall=True)
    return jsonify(rows)

@events.post("/events")
def create_event():
    uid = session["user_id"]
    eid = str(uuid.uuid4())
    data = request.json

    query("""
      INSERT INTO events (id,creator_id,title,venue,city,country,start_time,end_time,status)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'live')
    """,(eid,uid,data["title"],data["venue"],data["city"],data["country"],data["start"],data["end"]))

    return jsonify({"event_id":eid})
