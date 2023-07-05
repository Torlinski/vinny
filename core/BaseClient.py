# client.py
import logging

from core.Session import Session

logging.basicConfig(level=logging.DEBUG)


class BaseClient:
    def __init__(self):
        self.session = Session()

    def update(self, transcript):
        self.session.update(transcript)

    def set_status(self, status):
        self.session.set_status(status)
