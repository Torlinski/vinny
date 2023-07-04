import re
import logging

from objects.Session import Session

logging.basicConfig(level=logging.DEBUG)

class Session_GVariant(Session):

    def __init__(self):
        super.__init__()
        self.body = {0: ""}
        self.cur = 0
        self.command_history = []
        self.status = 'Not Used'

    def update(self, transcript):
        self.process(transcript)
        self.commands = [str(x) for x in self.command_history]
        self.paragraphs = []

    def process(self, command):
        func_name = None
        command = command.lower().strip()
        if command.startswith("new paragraph"):
            func_name = "new_paragraph"
            self.new_paragraph(command)
        elif command.startswith("select paragraph above"):
            func_name = "select_paragraph_above"
            self.select_paragraph_above(command)
        elif command.startswith("select paragraph below"):
            func_name = "select_paragraph_below"
            self.select_paragraph_below(command)
        elif command.startswith("undo"):
            func_name = "undo"
            self.undo(command)
        elif command.startswith("type"):
            func_name = "type"
            self.type(command)
        elif command.startswith("add"):
            func_name = "add"
            self.add(command)
        elif command.startswith("replace"):
            func_name = "replace"
            self.replace(command)
        else:
            func_name = "chatgpt"
            self.chatgpt(command)
        
        if func_name != 'undo':
            self.command_history.append((func_name, self.cur, self.body[self.cur]))

    def new_paragraph(self, _):
        self.cur += 1
        self.body[self.cur] = ""


    def select_paragraph_above(self, _):
        if self.cur > 0:
            self.cur -= 1


    def select_paragraph_below(self, _):
        if self.cur < len(self.body) - 1:
            self.cur += 1

    def undo(self, _):
        if self.command_history:
            last_command, self.cur, last_body = self.command_history.pop()
            self.body[self.cur] = last_body

    def type(self, command):
        sentence = command[5:]  # remove 'type ' from the start
        sentence = sentence[0].upper() + sentence[1:] #capitalize the first letter of the sentence
        if self.body[self.cur] != "":
            self.body[self.cur] += " "
        self.body[self.cur] += sentence + "."

    def replace(self, command):
        parts = command.split()
        if len(parts) >= 4 and parts[0] == "replace" and "with" in parts:
            replace_index = parts.index("with")
            replace_text = " ".join(parts[1:replace_index])
            with_text = " ".join(parts[replace_index + 1:])
            self.body[self.cur] = self.body[self.cur].replace(replace_text, with_text)

    def add(self, command):
        added_text = command[4:]  # remove 'add ' from the start
        self.body[self.cur] = self.body[self.cur].rsplit('.', 1)[0] + added_text + '.'
        self.ws_client.update_para(self.body[self.cur])  # Send the updated paragraph to the WebSocket server

    def chatgpt(self, command):
        pass
        #chat_gpt_client = ChatGPTClient()
        #new_text = chat_gpt_client.process(command)
        #self.body[self.cur] = new_text
