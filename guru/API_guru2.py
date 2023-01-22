from flask import Flask, request
import json
from guru2 import get_booking_page

app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        result = get_booking_page(data)
        result['success'] = True
        result['responseMessages'] = []
        return result



# host_IP = f'{input("Please inset IP:")}'
# host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    app.run(host='192.168.20.243', port='8087')

