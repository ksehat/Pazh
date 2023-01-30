import requests
import json
from flask import Flask
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_cors import CORS
import datetime as dt
from waitress import serve
from pymongo import MongoClient
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# app.config['DEBUG'] = True
socketio = SocketIO(app)
CORS(app)

# region DataBase handler
client = MongoClient()
mydatabase = client['history']
mycollection = mydatabase['messages']


# endregion


@socketio.on('connect')
def on_connect():
    print('Server received connection')


@socketio.on('disconnect')
def on_disconnect():
    print('disconnected')


@socketio.on('message')
def on_message(msg):
    # print(msg)
    send(msg, room=msg['room'])
    try:
        message = msg['msg']
    except:
        message = None
    record = {
        'user type': msg['usrType'],
        'room': msg['room'],
        'sender': msg['sender'],
        'location': msg['loc'],
        'message_text': message,
        'message_time': dt.datetime.now(),
    }
    mydatabase.mycollection.insert_one(record)


@socketio.on('join')
def on_join(data):
    room = data['room']
    token = data['token']
    r = requests.get(
        url='http://192.168.20.243:8083/api/Authentication/IsUserAuthorized',
        headers={'Authorization': f'Bearer {token}'})
    if json.loads(r.content)['success']:
        join_room(room)
        send('you join the room.', to=room)
    else:
        send({'error':True})


@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    send('you leave the room.', to=room)


if __name__ == "__main__":
    # socketio.run(app, allow_unsafe_werkzeug=True, host='192.168.40.155', port=8000)
    serve(app, host='192.168.40.155', port=8001, url_scheme='https', threads=5000, connection_limit=20000,
          channel_timeout=-1)
