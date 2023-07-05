import logging
import re

from word2number import w2n

logging.basicConfig(level=logging.DEBUG)

new_line_patterns = 'new line|newline|uline|new paragraph'
undo_patterns = 'go back|undo'
paragraph_patterns = (
    'paragraph\s(?:\d|one|two|three|for|four|five|six|seven|eight|nine|ten|to)'
)
chatgpt_patterns = 'please\s.*'
confirm_request_patterns = 'send request'
cancel_request_patterns = 'cancel request'


class Session:
    def __init__(self):
        self.status = 'Not Ready'
        self.versions = []
        self.paragraphs = [[]]
        self.commands = []
        self.input_text = ''
        self.index = 0
        self.chatgpt = ''

    def _new_line(self):
        if self.paragraphs[self.index] != ['']:
            self.index += 1
            self.paragraphs.insert(self.index, [''])
            self.commands.append(
                f'Added New Paragraph based on command {self.input_text}'
            )
            logging.info(self.commands[-1])

    def _undo(self):
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
        self.chatgpt = self.input_text
        self.commands.append(
            f'Creating chatgpt request from command: "{self.input_text}"'
        )
        logging.info(self.commands[-1])

    def _select_paragraph(self):
        if self.input_text[10:] == 'to':
            self.input_text = 'paragraph two'
        self.index = int(w2n.word_to_num(self.input_text[10:])) - 1
        self.commands.append(f'Set paragraph based on: "{self.input_text}"')
        logging.info(self.commands[-1])

    def set_status(self, status):
        self.status = status

    def _confirm_request(self):
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
        if self.chatgpt != '':
            self.chatgpt = ''
            self.commands.append(
                f'Received command to cancel request: "{self.input_text}"'
            )
            logging.info(self.commands[-1])

    def update(self, transcript):
        self.input_text = transcript.strip().lower()
        logging.info(f'"{self.input_text}"')

        if re.match(confirm_request_patterns, self.input_text):
            self._confirm_request()

        elif re.match(cancel_request_patterns, self.input_text):
            self._cancel_request()

        elif re.match(undo_patterns, self.input_text):
            self._undo()

        elif re.match(new_line_patterns, self.input_text):
            self._new_line()

        elif re.match(chatgpt_patterns, self.input_text):
            self._chatgpt()

        elif re.match(paragraph_patterns, self.input_text):
            self._select_paragraph()

        elif self.chatgpt == '':
            self.paragraphs[self.index].append(self.input_text)
            self.commands.append(f'Appended the text: "{self.input_text}"')
            logging.info(self.commands[-1])

    def emission(self):
        return {
            'paragraphs': self.paragraphs,
            'commands': self.commands,
            'index': self.index,
            'status': self.status,
            'chatgpt': self.chatgpt,
        }
