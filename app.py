from flask import Flask, request, jsonify
import uuid
from config import APP_SECRET
from db import query
from daraja import stk_push

app = Flask(__name__)
app.secret_key = APP_SECRET


@app.get("/")
def home():
    return "ChequePass API running"


# Create order + STK push
@app.post("/buy")
def buy_ticket():
    data = request.json
    phone = data["phone"]
    event_id = data["event_id"]
    amount = data["amount"]

    order_id = str(uuid.uuid4())

    query("""
        INSERT INTO orders (id, user_id, event_id, amount, status)
        VALUES (%s, %s, %s, %s, 'pending')
    """, (order_id, None, event_id, amount))

    stk = stk_push(phone, amount, order_id)

    return jsonify({
        "order_id": order_id,
        "stk": stk
    })


# M-Pesa callback
@app.post("/webhook/mpesa")
def mpesa_callback():
    payload = request.json
    body = payload["Body"]["stkCallback"]

    if body["ResultCode"] == 0:
        meta = body["CallbackMetadata"]["Item"]
        amount = meta[0]["Value"]
        receipt = meta[1]["Value"]

        order_id = body["CheckoutRequestID"]

        query("UPDATE orders SET status='paid' WHERE id=%s", (order_id,))

        query("""
            INSERT INTO payments (order_id, provider, provider_ref, amount, status, raw_callback)
            VALUES (%s,'mpesa',%s,%s,'success',%s)
        """, (order_id, receipt, amount, str(payload)))

    return jsonify({"ok": True})
