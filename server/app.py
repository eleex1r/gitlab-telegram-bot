from flask import Flask, request
from server.processor import process_event

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get('X-Gitlab-Event', 'Unknown')
    return process_event(event, data)
