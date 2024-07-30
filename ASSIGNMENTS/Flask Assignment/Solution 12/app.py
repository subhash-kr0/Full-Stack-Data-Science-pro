from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('client_event')
def handle_client_event(data):
    print('Received message from client:', data)
    emit('server_response', {'data': data['data']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
