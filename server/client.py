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

    def update_para(self, text):
        self.sio.emit('update_para', {'body': text})

    def update_command(self, command):
        self.sio.emit('update_command', {'command': command})

    def change_para(self, para):
        self.sio.emit('change_para', {'para': para})

    def disconnect(self):
        self.sio.disconnect()
