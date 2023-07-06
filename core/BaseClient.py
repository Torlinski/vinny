"""Base client class for future clients"""
import logging

from core.Session import Session

logging.basicConfig(level=logging.DEBUG)


class BaseClient:
    """Base Class"""

    def __init__(self):
        self.session = Session()

    def update(self, transcript: str):
        """Pass the latest transcript into the session."""
        self.session.update(transcript)

    def set_status(self, status: str):
        """Update session status based on input string."""
        self.session.set_status(status)
