from flask import Flask, request
import json
from sepehr_scraper import get_booking_sepehr

app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if (request.method == 'POST'):
        data = json.loads(request.data.decode('utf-8'))
        result = get_booking_sepehr(data)
        return result.to_json(orient='split', compression='infer')



# host_IP = f'{input("Please inset IP:")}'
# host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    app.run(host='192.168.40.155', port='2000')

