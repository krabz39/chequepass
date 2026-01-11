from flask import Blueprint, jsonify, session
import hashlib
from db import query

passes = Blueprint("passes", __name__)

@passes.get("/mypasses")
def my_passes():
    uid = session["user_id"]
    rows = query("SELECT id,qr_hash,status FROM passes WHERE owner_id=%s",(uid,),fetchall=True)
    return jsonify(rows)

@passes.get("/qr/<pid>")
def qr(pid):
    p = query("SELECT qr_hash FROM passes WHERE id=%s",(pid,),fetchone=True)
    return jsonify({"qr":p[0]})
