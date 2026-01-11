from flask import Flask, request, jsonify, render_template, session, redirect
import uuid

from config import APP_SECRET
from db import query
from daraja import stk_push

# Route blueprints
from routes.auth import auth
from routes.events import events
from routes.tickets import tickets
from routes.payments import payments
from routes.passes import passes
from routes.resale import resale
from routes.scan import scan
from routes.webhooks import webhooks


app = Flask(__name__)
app.secret_key = APP_SECRET

# --------------------------------
# Register blueprints
# --------------------------------
app.register_blueprint(auth)
app.register_blueprint(events)
app.register_blueprint(tickets)
app.register_blueprint(payments)
app.register_blueprint(passes)
app.register_blueprint(resale)
app.register_blueprint(scan)
app.register_blueprint(webhooks)

# --------------------------------
# UI ROUTES
# --------------------------------

@app.route("/")
def home():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/event/<event_id>")
def event_page(event_id):
    e = query(
        "SELECT id,title,venue,city,start_time FROM events WHERE id=%s",
        (event_id,),
        fetchone=True
    )
    if not e:
        return "Event not found", 404

    return render_template("event.html", event={
        "id": e[0],
        "title": e[1],
        "venue": e[2],
        "city": e[3],
        "start_time": e[4]
    })

@app.route("/creator")
def creator_page():
    return render_template("creator.html")

@app.route("/resale")
def resale_page():
    return render_template("resale.html")

@app.route("/scan")
def scan_page():
    return render_template("scan.html")

@app.route("/mypasses")
def my_passes_page():
    uid = session.get("user_id")
    if not uid:
        return redirect("/")

    p = query(
        "SELECT id, status FROM passes WHERE owner_id=%s",
        (uid,),
        fetchone=True
    )

    if not p:
        return "No passes yet"

    return render_template("pass.html", ticket_pass={
        "id": p[0],
        "status": p[1]
    })



# --------------------------------
# API ROUTES (Your original logic)
# --------------------------------

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
    """, (order_id, session.get("user_id"), event_id, amount))

    stk = stk_push(phone, amount, order_id)

    return jsonify({
        "order_id": order_id,
        "stk": stk
    })

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

@app.get("/health")
def health():
    return "OK"
