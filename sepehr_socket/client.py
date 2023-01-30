import socketio
from flask_socketio import send

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    # sio.send({'username':sio.sid})
    # sio.send(f"\nClient {sio.sid} connected...\n")
    pass

@sio.on('custom event')
def receive_custom(msg):
    print(msg)


@sio.on('disconnect')
def on_disconnect():
    # sio.send(f"\nClient {sio.sid} disconnected...\n")
    pass

@sio.on('message')
def handle_message(data):
    print('received message: ' + data if type(data)==str else f'{data}' )

sio.connect('http://192.168.40.155:8001')
message1 = {
    'room':'kanan',
    'sender':'hamed',
    'msg':'halet chetore?',
    'token':'sehat'
}
sio.emit('join', message1)
sio.send(message1)

while True:
    sio.send(f"{input()}")
# sio.wait() # cannot keyboard interrupt this
# sio.sleep(10)
# sio.disconnect()
