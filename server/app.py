from flask import Flask, request, jsonify
from server.processor import process_event
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.json
        event = request.headers.get('X-Gitlab-Event')
        
        if not event:
            return jsonify({'error': 'Missing X-Gitlab-Event header'}), 400
        
        response, status_code = process_event(event, data)
        return jsonify({'message': response}), status_code
    
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
