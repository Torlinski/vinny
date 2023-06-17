# client.py
import socketio

class Client:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.connect_to_server(server_url)

    def connect_to_server(self, server_url):
        @self.sio.event
        def connect():
            print("Connected to the server")

        @self.sio.event
        def disconnect():
            print("Disconnected from the server")

        self.sio.connect(server_url)

    def append(self, text):
        self.sio.emit('update', {'action': 'append', 'body': text})

    def replace(self, text):
        self.sio.emit('update', {'action': 'replace', 'body': text})

    def disconnect(self):
        self.sio.disconnect()

    def write_transcripts(self, responses):
        final = False
        buffer = ""
        for response in responses:
            for result in response.results:
                transcript = buffer
                buffer = result.alternatives[0].transcript
                if final:
                    self.append(transcript)
                    final = False
                else:
                    self.replace(transcript)
                if result.is_final:
                    self.replace(buffer)
                    buffer = ""
                    final = True
                    print(buffer)
