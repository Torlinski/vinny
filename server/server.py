from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
content = {0: ""}  # This variable will hold the current text content as a dictionary
cur = 0  # This variable will hold the current paragraph index

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
    """, content="\n".join([f"{k}: {v}" for k, v in content.items()]))


@socketio.on('update_para')
def handle_update_para(para):
    global content
    content[cur] = para.get('para')
    formatted_content = "\n".join([f"{k}: {v}" for k, v in content.items()])
    print(f"{formatted_content}, {para.get('para')}")
    emit('content', formatted_content, broadcast=True)

@socketio.on('change_cur')
def handle_change_cur(new_cur):
    global cur
    global content
    new_cur = int(new_cur.get('cur'))
    if content.get(new_cur) is None:
        content[new_cur] = ""
    cur = new_cur
    emit('paragraph', cur, broadcast=True)
    formatted_content = "\n".join([f"{k}: {v}" for k, v in content.items()])
    emit('content', formatted_content, broadcast=True)

@socketio.on('update_command')
def handle_update_command(command):
    emit('command', command.get('command'), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=8080)
