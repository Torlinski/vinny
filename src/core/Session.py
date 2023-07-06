"""Holds data related to a particular transcription session"""
import logging
import re

from word2number import w2n

from src.models import SessionPayload

logging.basicConfig(level=logging.DEBUG)

NEW_LINE_PATTERNS = r'new line|newline|uline|new paragraph'
UNDO_PATTERNS = r'go back|undo'
PARAGRAPH_PATTERNS = r'paragraph\s(?:\d|one|two|three|for|four|five|six|seven|eight|nine|ten|to)'
CHATGPT_PATTERNS = r'please\s.*'
CONFIRM_PATTERNS = r'send request'
CANCEL_PATTERNS = r'cancel request'


class Session:
    """Session object contains all data related to transcription command and text history"""

    def __init__(self):
        self.status = 'Not Ready'
        self.versions = []
        self.paragraphs = [[]]
        self.commands = []
        self.input_text = ''
        self.index = 0
        self.chatgpt = ''

    def _new_line(self):
        """Interprets transcript as new paragraph command"""
        if self.paragraphs[self.index] != ['']:
            self.index += 1
            self.paragraphs.insert(self.index, [''])
            self.commands.append(
                f'Added New Paragraph based on command {self.input_text}'
            )
            logging.info(self.commands[-1])

    def _undo(self):
        """Interprets transcript as undo command"""
        if self.paragraphs[self.index] == ['']:
            self.paragraphs.pop(self.index)
            self.commands.append(f'Removed paragraph {self.index+1}')
            self.index -= 1
            logging.info(self.commands[-1])
        else:
            removed_text = self.paragraphs[self.index].pop()
            self.commands.append(f'Removed the text: "{removed_text}"')
            logging.info(self.commands[-1])

    def _chatgpt(self):
        """Interprets transcript as chatgpt request"""
        self.chatgpt = self.input_text
        self.commands.append(
            f'Creating chatgpt request from command: "{self.input_text}"'
        )
        logging.info(self.commands[-1])

    def _select_paragraph(self):
        """Interprets transcript as paragraph index"""
        if self.input_text[10:] == 'to':
            self.input_text = 'paragraph two'
        self.index = int(w2n.word_to_num(self.input_text[10:])) - 1
        self.commands.append(f'Set paragraph based on: "{self.input_text}"')
        logging.info(self.commands[-1])

    def set_status(self, status: str):
        """Set status of session"""
        self.status = status

    def _confirm_request(self):
        """Interprets transcript as confirmation to send chatgpt request"""
        if self.chatgpt != '':
            self.chatgpt = ''
            self.commands.append(
                f'Received command to send request: "{self.input_text}"'
            )
            logging.info(self.commands[-1])
            # chat_gpt_client = ChatGPTClient()
            # new_text = chat_gpt_client.process(command)
            # self.paragraphs[self.index] = [new_text]

    def _cancel_request(self):
        """Interprets transcript as user wish to cancel chatgpt request"""
        if self.chatgpt != '':
            self.chatgpt = ''
            self.commands.append(
                f'Received command to cancel request: "{self.input_text}"'
            )
            logging.info(self.commands[-1])

    def update(self, transcript: str):
        """Receive transcript and determines what to do with it"""
        self.input_text = transcript.strip().lower()
        logging.info('"%s"', self.input_text)

        if re.match(CONFIRM_PATTERNS, self.input_text):
            self._confirm_request()

        elif re.match(CANCEL_PATTERNS, self.input_text):
            self._cancel_request()

        elif re.match(UNDO_PATTERNS, self.input_text):
            self._undo()

        elif re.match(NEW_LINE_PATTERNS, self.input_text):
            self._new_line()

        elif re.match(CHATGPT_PATTERNS, self.input_text):
            self._chatgpt()

        elif re.match(PARAGRAPH_PATTERNS, self.input_text):
            self._select_paragraph()

        elif self.chatgpt == '':
            self.paragraphs[self.index].append(self.input_text)
            self.commands.append(f'Appended the text: "{self.input_text}"')
            logging.info(self.commands[-1])

    def emission(self) -> SessionPayload:
        """Provides session data for external use"""
        return SessionPayload(
            **{
                'paragraphs': self.paragraphs,
                'commands': self.commands,
                'index': self.index,
                'status': self.status,
                'chatgpt': self.chatgpt,
            }
        )
