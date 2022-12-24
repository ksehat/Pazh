from flask import Flask, request
import json
from guru2 import get_booking_page
from json_parser import json_parser

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        result = get_booking_page('THR', 'AWZ', 1, 0, 0, '1401-10-01', '1401-10-02')
        return result
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        json_parser(data)

        print('')



host_IP = f'{input("Please inset IP:")}'
host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    app.run(host=host_IP, port=host_port)

