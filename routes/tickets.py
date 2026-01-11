from flask import Blueprint, request, jsonify
import uuid
from db import query

tickets = Blueprint("tickets", __name__)

@tickets.post("/tickets")
def create_ticket():
    t = request.json
    tid = str(uuid.uuid4())

    query("""
      INSERT INTO tickets (id,event_id,name,price,supply,resale_allowed,royalty_percent)
      VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,(tid,t["event_id"],t["name"],t["price"],t["supply"],t["resale"],t["royalty"]))

    return jsonify({"ticket_id":tid})
