from flask import Blueprint, request
import uuid, hashlib
from db import query

webhooks = Blueprint("webhooks", __name__)

@webhooks.post("/webhook/mpesa")
def mpesa():
    payload = request.json
    body = payload["Body"]["stkCallback"]

    if body["ResultCode"] == 0:
        order_id = body["CheckoutRequestID"]

        order = query("SELECT user_id FROM orders WHERE id=%s",(order_id,),fetchone=True)
        pid = str(uuid.uuid4())
        qr = hashlib.sha256((pid+order_id).encode()).hexdigest()

        query("INSERT INTO passes (id,order_id,owner_id,qr_hash,status) VALUES (%s,%s,%s,%s,'active')",
              (pid,order_id,order[0],qr))

    return {"ok":True}
