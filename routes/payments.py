from flask import Blueprint, request, jsonify, session
import uuid
from db import query
from daraja import stk_push

payments = Blueprint("payments", __name__)

@payments.post("/pay")
def pay():
    uid = session["user_id"]
    data = request.json
    oid = str(uuid.uuid4())

    query("""
      INSERT INTO orders (id,user_id,event_id,amount,status)
      VALUES (%s,%s,%s,%s,'pending')
    """,(oid,uid,data["event_id"],data["amount"]))

    stk = stk_push(data["phone"], data["amount"], oid)
    return jsonify({"order_id":oid,"stk":stk})
