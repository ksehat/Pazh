import socketio
from flask_socketio import send


class SocketIO_Class:
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.event('connect', self.on_connect)
        self.sio.event('disconnect', self.on_disconnect)
        self.sio.on('message', self.handle_message)

    def on_connect(self):
        # sio.send({'username':sio.sid})
        self.sio.connect('http://192.168.40.155:8001')

    def on_disconnect(self):
        self.sio.send(f"\nClient {self.sio.sid} disconnected...\n")

    def handle_message(self, msg):
        print('received message: ' + f'{msg}')

    def join(self, msg):
        self.sio.emit('join', msg)

    def send_msg(self, msg, room):
        self.sio.send({'msg': msg, 'room': room})



