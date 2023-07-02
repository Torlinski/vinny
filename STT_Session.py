

class STT_Session:

    def __init__(self):
        self.text = []
        self.commands = []

    def update(self, raw_text):
        input_text = raw_text.strip().lower()
        print(f'"{input_text}"')

        if input_text in ['new line', 'newline', 'uline', 'new paragraph']:
            if self.text[-1]!='\n':
                self.text.append('\n\n')
                self.commands.append(f'Added New Line based on command {input_text}')
                print(self.commands[-1])
            else:
                self.commands.append(f'Ignored Extra New Line based on command {input_text}')
                print(self.commands[-1])
        elif input_text == 'go back':
            print(f'Removing last item based on command {input_text}')
            self.commands.append(f'Removed the text: "{self.text.pop()}"')
        
        else:
            self.text.append(input_text.strip())
            self.commands.append(f'Appended the text: "{self.text[-1]}"')
            
    def get_text(self):
        previous_text = '<span>'+' '.join(self.text[:-1])+'</span>'
        last_text = '<span style="color: #80a2bf;">'+' '+self.text[-1]+'</span>'
        return previous_text+last_text
    

    def get_comlist(self):
        comlist = '<ul>'+''.join(['<li>'+x+'</li>' for x in self.commands[::-1]])+'</ul>'
        return comlist