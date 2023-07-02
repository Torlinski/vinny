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

    def update_para(self, para):
        self.sio.emit('update_para', {'para': para})

    def update_comlist(self, comlist):
        self.sio.emit('update_comlist', {'comlist': comlist})

    def update_status(self, status):
        self.sio.emit('update_status', {'status': status})

    def update_command(self, command):
        self.sio.emit('update_command', {'command': command})

    def change_cur(self, cur):
        self.sio.emit('change_cur', {'cur': cur})

    def disconnect(self):
        self.sio.disconnect()
