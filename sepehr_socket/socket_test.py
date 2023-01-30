import random
import time

from client_class import SocketIO_Class
from concurrent.futures import ThreadPoolExecutor


def send_message(driver, msg, room):
    driver.send_msg(msg, room)

num_of_drivers = 100
clients_dict = {}
drivers_dict = {}
for i in range(num_of_drivers):
    clients_dict[f'client{i}'] = [SocketIO_Class(), f'client{i}']
    drivers_dict[f'driver{i}'] = [SocketIO_Class(), f'client{i}']
for k, v in clients_dict.items():
    v[0].on_connect()
    v[0].join({'msg': f'{k} joined the room {v[1]}', 'room': v[1]})
    # v.send_msg({'msg': 'salam', 'room': client1.sio.sid})
for k, v in drivers_dict.items():
    v[0].on_connect()
    v[0].join({'msg': f'{k} joined the room {v[1]}', 'room': v[1]})


driver_list = [x[0] for x in drivers_dict.values()]
msg_list = list(clients_dict.keys())
rooms_list = list(clients_dict.keys())
for _ in range(100):
    time.sleep(3)
    with ThreadPoolExecutor() as executor:
        result = executor.map(send_message, driver_list, msg_list, rooms_list)
