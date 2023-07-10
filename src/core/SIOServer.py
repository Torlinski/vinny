"""Socket IO Client contains code for sending session data to websocket"""
import logging

from src.core.BaseServer import BaseServer
from src.core.HTMLInterface import HTMLInterface

logging.basicConfig(level=logging.DEBUG)


class SIOServer(BaseServer):
    """Extends Client base class, performs extra functions around session updates."""

    def __init__(self, sio):
        super().__init__()
        self.sio = sio

    def update(self, transcript: str):
        """Update session with transcript and emit data"""
        super().update(transcript)
        payload = self.session.emission()
        print("WE SHOULD BE BROADCASING")
        self.sio.emit('content', HTMLInterface.html_text(payload), broadcast=True)
        self.sio.emit('commands', HTMLInterface.html_commands(payload), broadcast=True)
        self.sio.emit('status', payload.status, broadcast=True)
        self.sio.emit('chatgpt', HTMLInterface.html_chatgpt(payload), broadcast=True)

    def set_status(self, status: str):
        """Update session status and emit data"""
        super().set_status(status)
        self.sio.emit('update', self.session.emission().model_dump())

    def disconnect(self):
        """Disconnect from websocket server"""
        self.sio.disconnect()