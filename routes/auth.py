from flask import Blueprint, request, session, jsonify
import uuid
from db import query

auth = Blueprint("auth", __name__)

@auth.post("/login")
def login():
    phone = request.json["phone"]
    country = request.json.get("country","")

    user = query("SELECT id FROM users WHERE phone=%s", (phone,), fetchone=True)

    if not user:
        uid = str(uuid.uuid4())
        query("INSERT INTO users (id, phone, country) VALUES (%s,%s,%s)",
              (uid, phone, country))
    else:
        uid = user[0]

    session["user_id"] = uid
    return jsonify({"user_id": uid})
