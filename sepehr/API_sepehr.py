from flask import Flask, request, jsonify
import json
from sepehr_scraper import get_booking_sepehr
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if (request.method == 'POST'):
        data = json.loads(request.data)
        result = get_booking_sepehr(data)
        return jsonify({'data': (result.to_json(orient='records', force_ascii=False))}).json



# host_IP = f'{input("Please inset IP:")}'
# host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    serve(app, host='192.168.40.155', port='3000')

