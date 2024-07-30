from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def background_thread():
    """Example of how to send server-generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('notification', {'data': f'Notification {count}'}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
