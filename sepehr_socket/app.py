from waitress import serve
import socketio


sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    my_message(sid, {'Test': 'Message'})


@sio.event
def my_message(sid, data):
    sio.send(data)
    print('Send message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # serve(app, host='192.168.40.155', port=8080)
    socketio.run('192.168.40.155:8080')