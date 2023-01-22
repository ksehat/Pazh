from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import requests
import json

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info={
        'title': LazyString(lambda: 'My first Swagger UI document'),
        'version': LazyString(lambda: '0.1'),
        'description': LazyString(
            lambda: 'This document contains all APIs for Mobile.'),
    },
    host=LazyString(lambda: '192.168.40.155:5000')
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'request_token',
            "route": '/swagger/mobile/v2/swagger.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)


@swag_from()
@app.route("/api/Authentication/RequestToken", methods=['POST'])
def request_token():
    """
    Echo back the token and expir date of posted parameters.
    ---
    tags:
      - RequestToken

    parameters:
      - in: body
        name: body
        description: JSON parameters.
        schema:
          properties:
            username:
              type: string
              description: username
              example: Alice
            password:
              type: string
              description: password
              example: Smith145
            applicationType:
              type: integer
              example: 960
            iP:
              type: string
              example: 192.168.40.155

    responses:
      500:
        description: Error The number is not integer!
      200:
        # description: Output
        schema:
          id: Success
          description: succsess
          # example: succsess
          # properties:
          #   token:
          #     type: string
          #     description: Token
          #   expire_date:
          #     type: string
          #     description: date
    """
    if (request.method == 'POST'):
        data = json.loads(request.data)
        dict1 = {
            "username": f"{data['username']}",
            "password": f"{data['password']}",
            "applicationType": 961,
            "iP": "1365"
        }

        r = requests.post(url='http://192.168.20.243:8081/api/Authentication/RequestToken', json=dict1)
        token = json.loads(r.text)['token']
        expire_date = json.loads(r.text)['expires']
        return jsonify({'token':token, 'expire_date':expire_date})


if __name__ == '__main__':
    app.run(host='192.168.40.155', port='5000')
