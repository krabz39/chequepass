from flask import Blueprint, request, jsonify, session
import uuid
from db import query

resale = Blueprint("resale", __name__)

@resale.post("/resell")
def list_resale():
    pid = request.json["pass_id"]
    price = request.json["price"]
    uid = session["user_id"]

    rid = str(uuid.uuid4())
    query("INSERT INTO resales (id,pass_id,seller_id,price,status) VALUES (%s,%s,%s,%s,'listed')",
          (rid,pid,uid,price))
    return jsonify({"resale_id":rid})
