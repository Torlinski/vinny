import openai

openai.api_key = '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'

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)

# create a chat completion
with open("chatgpt/prompt.txt") as f:
    prompt = f.read()
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role": "user",
        "content": prompt,
        }],
    temperature=0,
)

# print the chat completion
print(chat_completion.choices[0].message.content)