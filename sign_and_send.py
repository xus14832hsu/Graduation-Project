# sign_and_send.py - RSA簽章後POST給驗證伺服器
import time
import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import requests

# 載入私鑰（私鑰一定不能給別人）
with open("private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# 組合訊息
chat_id = "987654321"
timestamp = str(int(time.time()))
message = f"{chat_id}:{timestamp}".encode()

# 計算 SHA-256 Hash 並簽章
h = SHA256.new(message)
signature = pkcs1_15.new(private_key).sign(h)
signature_b64 = base64.b64encode(signature).decode()

# 發送到驗證端（樹莓派上的 Flask 伺服器）
url = "http://192.168.0.188:5000/verify"
payload = {
    "chat_id": chat_id,
    "timestamp": timestamp,
    "signature": signature_b64
}

response = requests.post(url, json=payload)  # 用 JSON 傳
print(response.status_code, response.text)
