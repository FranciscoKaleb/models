from flask import Flask, render_template, request, jsonify, session
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from qwenchatbotapi import load_model, get_response

app = Flask(__name__)
app.secret_key = 'qwen-chat-secret-key'

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
