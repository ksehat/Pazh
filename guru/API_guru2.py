from flask import Flask, request, json
from guru2 import get_booking_page

# import request

# creating a Flask app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        result = get_booking_page('THR', 'AWZ', 1, 0, 0, '1401-10-01', '1401-10-02')
        return result
    if (request.method == 'POST'):
        print('')


host_IP = f'{input("Please inset IP:")}'
host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    app.run(host=host_IP, port=host_port)
