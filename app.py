from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sys
import os

import secrets

API_KEY = os.environ.get('CHAT_API_KEY', 'thebomb123')

def require_api_key(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if not key or not secrets.compare_digest(key, API_KEY):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from qwenchatbotapi import load_model, get_response

app = Flask(__name__)
app.secret_key = 'qwen-chat-secret-key'
CORS(app, supports_credentials=True)

load_model()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat')
def chat():
    session.setdefault('history', [])
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
@require_api_key
def api_chat():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400

    history = session.get('history', [])
    reply = get_response(history, user_input)
    session['history'] = history
    session.modified = True

    return jsonify({'reply': reply})

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    session['history'] = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(debug=False)
