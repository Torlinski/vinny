from typing import Any, Dict

from flask import Flask
from flask_socketio import SocketIO

from .blueprints.index import index

def create_app():
    app = Flask(__name__)
    app.register_blueprint(index)
    socketio = SocketIO(app)

    @socketio.on('edit')
    def handle_edit(edit: Dict[str, Any]):
        """Listen for messages on websocket containing user edits"""
        # do stuff with the edit

    return app, socketio