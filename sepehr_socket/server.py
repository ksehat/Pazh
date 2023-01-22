from flask import Flask
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_cors import CORS
import time
from waitress import serve


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# app.config['DEBUG'] = True
socketio = SocketIO(app)
CORS(app)


@socketio.on('connect')
def on_connect():
    print('Server received connection')


@socketio.on('disconnect')
def on_disconnect():
    print('disconnected')


@socketio.on('message')
def on_message(msg):
    print(msg)
    send({'msg':msg['msg'],'loc':msg['loc']['lat']+ ',' +msg['loc']['long']},room=msg['room'])


@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    send('you join the room.', to=room)


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    send('you leave the room.', to=room)


def join_room_local(room):
    join_room(room)


if __name__ == "__main__":
    # socketio.run(app, allow_unsafe_werkzeug=True, host='192.168.40.155', port=8000)
    serve(app, host='192.168.40.155', port=8001, threads=8)
