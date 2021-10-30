import json
import logging

from datetime import datetime

from flask import Flask, Response
from flask import request, render_template, jsonify
from flask_cors import CORS

from middleware.service_helper import _get_service_by_name

import utils.rest_utils as rest_utils

app = Flask(__name__)
CORS(app)


@app.route('/users', methods=["GET", "POST"])
def get_users():
    try:
        inputs = rest_utils.RESTContext(request)
        service = _get_service_by_name("user_service")
        if service is not None:
            if inputs.method == 'GET':
                res = service.find_by_template(inputs.args, inputs.fields, inputs.limit, inputs.offset)
                if res is not None:
                    res = json.dumps(res, default = str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')
            else:
                rsp = Response("NOT IMPLEMENTED", status=501)
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /users\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)