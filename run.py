from src.core.main import main
from src import create_app

app, socketio = create_app()

if __name__ == '__main__':
    socketio.start_background_task(main, socketio)
    socketio.run(app, host='127.0.0.1', port=8080, debug=True)