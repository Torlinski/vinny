from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from utils.HTML_Interface import HTML_Interface

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('home.html')

@socketio.on('update')
def handle_update_status(update):
    emit('content', HTML_Interface.html_text(update), broadcast=True)
    emit('commands', HTML_Interface.html_commands(update), broadcast=True)
    emit('status', update.get('status'), broadcast=True)
    emit('chatgpt', HTML_Interface.html_chatgpt(update), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=8080, debug=True)
