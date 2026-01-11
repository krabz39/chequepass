from flask import Blueprint, request, jsonify
from db import query
import uuid

scan = Blueprint("scan", __name__)

@scan.post("/scan")
def scan_qr():
    qr = request.json["qr"]

    p = query("SELECT id,status FROM passes WHERE qr_hash=%s",(qr,),fetchone=True)

    if not p or p[1]!="active":
        return jsonify({"valid":False})

    query("UPDATE passes SET status='used' WHERE id=%s",(p[0],))
    query("INSERT INTO scans (id,pass_id,result) VALUES (%s,%s,'valid')",
          (str(uuid.uuid4()),p[0]))

    return jsonify({"valid":True})
