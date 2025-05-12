# verify_server.py - 在樹莓派上運行的 Flask 驗證伺服器
from flask import Flask, request
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

app = Flask(__name__)

# 載入公鑰（跟 ESP32 用的一樣）
with open("public.pem", "r") as f:
    public_key = RSA.import_key(f.read())

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    if not data:
        return "Bad Request", 400

    chat_id = data.get("chat_id")
    timestamp = data.get("timestamp")
    signature_b64 = data.get("signature")

    if not chat_id or not timestamp or not signature_b64:
        return "Missing fields", 400

    message = f"{chat_id}:{timestamp}".encode("utf-8")

    try:
        signature = base64.b64decode(signature_b64)
    except Exception:
        return "Invalid signature format", 400

    hash_obj = SHA256.new(message)
    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        return "Signature valid!", 200
    except (ValueError, TypeError):
        return "Invalid signature.", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
