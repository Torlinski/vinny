# client.py
import logging

from objects.Session import Session

logging.basicConfig(level=logging.DEBUG)

class Client():
    def __init__(self, session: Session):
        self.session = session
         
    def update(self, transcript):
        self.session.update(transcript)

    def set_status(self, status):
        self.session.set_status(status)
