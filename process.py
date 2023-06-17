class CommandProcessor:
    def __init__(self):
        self.body = {0: ""}
        self.cur = 0

    def process(self, command):
        if command.startswith("new paragraph"):
            self.new_paragraph(command)
        elif command.startswith("select paragraph above"):
            self.select_paragraph_above(command)
        elif command.startswith("select paragraph below"):
            self.select_paragraph_below(command)
        elif command.startswith("undo"):
            self.undo(command)
        elif command.startswith("type"):
            self.type(command)
        elif command.startswith("replace"):
            self.replace(command)
        else:
            self.unknown_command(command)

    def new_paragraph(self, command):
        print("New paragraph command received: ", command)
        self.cur += 1
        self.body[self.cur] = ""
        
    def select_paragraph_above(self, command):
        print("Select paragraph above command received: ", command)
        if self.cur - 1 in self.body:
            self.cur -= 1

    def select_paragraph_below(self, command):
        print("Select paragraph below command received: ", command)
        if self.cur + 1 in self.body:
            self.cur += 1

    def undo(self, command):
        print("Undo command received: ", command)
        # Logic to undo the last command.

    def type(self, command):
        print("Type command received: ", command)
        # Logic to add text to the current paragraph.

    def replace(self, command):
        print("Replace command received: ", command)
        # Logic to replace text in the current paragraph.

    def unknown_command(self, command):
        print("Unknown command received: ", command)
