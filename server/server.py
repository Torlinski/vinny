from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
content = {0: ""}  # This variable will hold the current text content as a dictionary
status = ''
cur = 0  # This variable will hold the current paragraph index

items = ['', 'Hello', 'How', 'Are', 'You']
progress = []
holder = []

@app.route('/')
def index():
    return render_template('home.html')


@socketio.on('update_para')
def handle_update_para(para):
    global content
    global holder
    holder.append(para.get('para'))
    content[cur] = para.get('para')
    formatted_content = "\n".join([f"{k}: {v}" for k, v in content.items()])
    print(f"{formatted_content}, {para.get('para')}")
    emit('content', formatted_content, broadcast=True)


@socketio.on('update_status')
def handle_update_status(status):
    emit('status', status.get('status'), broadcast=True)

@socketio.on('update_comlist')
def handle_update_comlist(comlist):
    emit('comlist', comlist.get('comlist'), broadcast=True)

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
    socketio.run(app, host="127.0.0.1", port=8080, debug=True)
