"""Flask server for front-end"""
from typing import Any, Dict

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from src.frontend.HTMLInterface import HTMLInterface
from src.models import SessionPayload

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    """Return index page"""
    return render_template('index.html')


@socketio.on('update')
def handle_update_status(update: Dict[str, Any]):
    """Listen for messages on websocket containing session data to broadcast"""
    update = SessionPayload(**update)
    emit('content', HTMLInterface.html_text(update), broadcast=True)
    emit('commands', HTMLInterface.html_commands(update), broadcast=True)
    emit('status', update.status, broadcast=True)
    emit('chatgpt', HTMLInterface.html_chatgpt(update), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8080, debug=True)
