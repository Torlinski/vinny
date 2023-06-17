from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
content = ""  # This variable will hold the current text content

@app.route('/')
def index():
    # Render the index template with the current content
    return render_template_string("""
        <!doctype html>
        <html>
            <head>
                <title>vinny</title>
                <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.3/socket.io.min.js"></script>
                <script>
                document.addEventListener("DOMContentLoaded", function() {
                    var socket = io.connect('http://' + document.domain + ':' + location.port);
                    socket.on('content', function(content) {
                        document.getElementById('content').innerText = content;
                    });
                    socket.on('paragraph', function(paragraph) {
                        var paras = document.getElementById('content').children;
                        for (var i = 0; i < paras.length; i++) {
                            paras[i].style.backgroundColor = i == paragraph ? 'yellow' : 'transparent';
                        }
                    });
                    socket.on('command', function(command) {
                        document.getElementById('command').innerText = command;
                    });
                });
                </script>
                <style>
                #content {
                    white-space: pre-line;
                }
                #command {
                    border: 1px solid black;
                    padding: 10px;
                    margin-top: 10px;
                }
                </style>
            </head>
            <body>
                <div id="content">{{ content }}</div>
                <div id="command"></div>
            </body>
        </html>
    """, content=content)


@socketio.on('update_para')
def handle_update_para(para):
    global content
    content[para.get('paragraph')] = para.get('content')
    emit('content', content, broadcast=True)

@socketio.on('change_para')
def handle_change_para(para):
    emit('paragraph', para.get('paragraph'), broadcast=True)

@socketio.on('update_command')
def handle_update_command(command):
    emit('command', command.get('command'), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=8080)
