import logging

logging.basicConfig(level=logging.DEBUG)

class Session:

    def __init__(self):
        self.status = 'Not Ready'
        self.versions = []
        self.paragraphs = [[]]
        self.commands = []
        self.input_text = ''
        self.index = 0
        self.chatgpt = ''

    def update(self, transcript):
        pass

    def set_status(self, status):
        pass

    def emission(self):
        return {'paragraphs': self.paragraphs, 'commands': self.commands, 'index': self.index, 'status': self.status, 'chatgpt': self.chatgpt}