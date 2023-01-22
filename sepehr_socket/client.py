import socketio
from flask_socketio import send

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    # sio.send({'username':sio.sid})
    sio.send(f"\nClient {sio.sid} connected...\n")


@sio.on('custom event')
def receive_custom(msg):
    print(msg)


@sio.on('disconnect')
def on_disconnect():
    sio.send(f"\nClient {sio.sid} disconnected...\n")


@sio.on('message')
def handle_message(data):
    print('received message: ' + data)

sio.connect('http://192.168.40.155:8001')
sio.emit('join', {'username': sio.sid})

while True:
    sio.send(f"{input()}")
# sio.wait() # cannot keyboard interrupt this
# sio.sleep(10)
# sio.disconnect()
