"""Socket IO Client contains code for sending session data to websocket"""
import logging

import socketio

from src.core.BaseClient import BaseClient

logging.basicConfig(level=logging.DEBUG)


class SIOClient(BaseClient):
    """Extends Client base class, performs extra functions around session updates."""

    def __init__(self, server_url: str):
        super().__init__()
        self.sio = socketio.Client()
        self._connect_to_server(server_url)

    def _connect_to_server(self, server_url: str):
        """Connect to websocket server"""

        @self.sio.event
        def connect():
            logging.debug('Connected to the server')

        @self.sio.event
        def disconnect():
            logging.debug('Disconnected from the server')

        self.sio.connect(server_url)

    def update(self, transcript: str):
        """Update session with transcript and emit data"""
        super().update(transcript)
        self.sio.emit('update', self.session.emission().model_dump())

    def set_status(self, status: str):
        """Update session status and emit data"""
        super().set_status(status)
        self.sio.emit('update', self.session.emission().model_dump())

    def disconnect(self):
        """Disconnect from websocket server"""
        self.sio.disconnect()
