import requests
from config import *

def send_wamd(phone, amount, reference):
    payload = {
        "api_key": WAMD_API_KEY,
        "phone": phone,
        "amount": amount,
        "reference": reference,
        "callback": WAMD_CALLBACK_URL
    }

    r = requests.post("https://wamd.api/pay", json=payload)
    return r.json()
