import hmac
import hashlib
import requests
import time

key = b'123456789'
chat_id = '987654321'
timestamp = str(int(time.time()))
message = f'{chat_id}:{timestamp}'.encode('utf-8')

signature = hmac.new(key, message, hashlib.sha256).hexdigest()

url = 'http://192.168.0.188:5000/signature'
payload = {
    'chat_id': chat_id,
    'timestamp': timestamp,
    'signature': signature
}

response = requests.post(url, data=payload)
print(response.status_code, response.text)

print('Payload:', payload)
print('URL:', url)
print('Response:', response.status_code)
print('Response Text:', response.text)
