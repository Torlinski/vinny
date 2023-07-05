import openai

if __name__ == '__main__':
    with open('api_key.txt') as f:
        openai.api_key = f.read()

    # list models
    models = openai.Model.list()

    # print the first model's id
    print(models.data[0].id)

    # create a chat completion
    with open('chatgpt/prompt.txt') as f:
        prompt = f.read()
    chat_completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        temperature=0,
    )

    # print the chat completion
    print(chat_completion.choices[0].message.content)


class ChatGPTClient:   # auto generated crap
    def __init__(self):
        self.chat_history = []
        # self.chat_history.append(prompt)
        # self.chat_history.append(chat_completion.choices[0].message.content)
        # self.chat_history.append("")

    def chatgpt(self, command):
        self.chat_history.append(command)
        chat_completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            prompt='\n'.join(self.chat_history),
            temperature=0,
        )
        self.chat_history.append(chat_completion.choices[0].message.content)
        self.chat_history.append('')
        return chat_completion.choices[0].message.content

    def undo(self, command):
        self.chat_history.pop

    def process(self, command):
        print('Command sent to chatgpt: ' + command)
        return command
