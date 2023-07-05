"""Socket IO Client contains code for sending session data to websocket"""
import logging

import socketio

from core.BaseClient import BaseClient

logging.basicConfig(level=logging.DEBUG)


class SIOClient(BaseClient):
    """
    Extends Client base class, performs extra functions around session updates.

    Args:
        Client (_type_): _description_
    """

    def __init__(self, server_url: str):
        super().__init__()
        self.sio = socketio.Client()
        self._connect_to_server(server_url)

    def _connect_to_server(self, server_url: str):
        @self.sio.event
        def connect():
            logging.debug('Connected to the server')

        @self.sio.event
        def disconnect():
            logging.debug('Disconnected from the server')

        self.sio.connect(server_url)

    def update(self, transcript: str):
        super().update(transcript)
        self.sio.emit('update', self.session.emission())

    def set_status(self, status: str):
        super().set_status(status)
        self.sio.emit('update', self.session.emission())

    def disconnect(self):
        self.sio.disconnect()
