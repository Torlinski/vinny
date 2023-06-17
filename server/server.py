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
                });
                </script>
                <style>
                #content {
                    white-space: pre-line;
                }
                </style>
            </head>
            <body>
                <pre id="content">{{ content }}</pre>
            </body>
        </html>
    """, content=content)

@socketio.on('update')
def handle_update(update):
    global content
    action = update.get('action')
    body = update.get('body')
    
    # Add a newline to the body if it doesn't end with one
    if not body.endswith('\n'):
        body += '\n'
    
    if action == 'append':
        # Append the body to the content
        content += body
    elif action == 'replace':
        # Replace the last line in the content with the body
        last_line_start = content.rfind('\n', 0, -1) + 1  # -2 to skip the last newline
        content = content[:last_line_start] + body
    else:
        return
    
    # Emit the new content to all connected clients
    emit('content', content, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=8080)
