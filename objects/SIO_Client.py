# client.py
import socketio
import logging

from objects.Client import Client
from objects.Session import Session


logging.basicConfig(level=logging.DEBUG)

class SIO_Client(Client):
    def __init__(self, session, server_url):
        super().__init__(session)
        self.sio = socketio.Client()
        self.connect_to_server(server_url)
              
    def connect_to_server(self, server_url):
        @self.sio.event
        def connect():
            logging.debug("Connected to the server")

        @self.sio.event
        def disconnect():
            logging.debug("Disconnected from the server")

        self.sio.connect(server_url)

    def update(self, transcript):
        super().update(transcript)
        self.sio.emit('update', self.session.emission())

    def set_status(self, status):
        super().set_status(status)
        self.sio.emit('update', self.session.emission())

    def disconnect(self):
        self.sio.disconnect()
