import qrcode
from io import BytesIO
from flask import send_file

def generate_qr_image(qr_hash):
    img = qrcode.make(qr_hash)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
