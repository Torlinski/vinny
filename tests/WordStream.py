class WordStream:
    """Creates a generator for word chunks."""

    def __init__(self, chunks):
        self.chunks = chunks

    def generator(self):
        while True and len(self.chunks) > 0:
            chunk = self.chunks.pop(0)
            yield chunk
