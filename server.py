import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)

SECRET_KEY = b'123456789'

def compute_hmac_sha256(key: bytes, message: str) -> str:
    h = hmac.new(key, message.encode('utf-8'), hashlib.sha256)
    return h.hexdigest()

@app.route('/signature', methods=['POST'])
def signature():
    chat_id = request.form.get('chat_id')
    timestamp = request.form.get('timestamp')
    received_signature = request.form.get('signature')

    if not chat_id or not timestamp or not received_signature:
        return 'Missing parameters.', 400

    message = f'{chat_id}:{timestamp}'
    print(f'Received message: {message}')
    print(f'Received signature: {received_signature}')

    computed_signature = compute_hmac_sha256(SECRET_KEY, message)
    print(f'Computed signature: {computed_signature}')

    if hmac.compare_digest(computed_signature, received_signature):
        return 'Signature valid!', 200
    else:
        return 'Invalid signature.', 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
