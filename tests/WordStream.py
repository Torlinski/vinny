"""Provides generator for words from a stream for test purposes"""
from typing import List


class WordStream:
    """Creates a generator for word chunks."""

    def __init__(self, chunks: List[str]):
        self.chunks = chunks

    def generator(self):
        """Retrieve input words as generator object"""
        while len(self.chunks) > 0:
            chunk = self.chunks.pop(0)
            yield chunk
