from flask import Flask, Response, request, render_template, jsonify
import database_services.RDBService as d_service
from flask_cors import CORS
import json

import logging

import utils.rest_utils as rest_utils

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.UsersResource.user_service import UserResource
from application_services.AddressResource.address_service import AddressResource



app = Flask(__name__)
CORS(app)


@app.route('/users', methods=["GET", "POST"])
def get_users():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = UserResource.get_by_template(None)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "POST":
            data = input.data
            res = UserResource.add_by_template(data)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/users', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/users/<userID>', methods=["GET", "PUT", "DELETE"])
def get_users_by_userID(userID):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = UserResource.get_by_template({'ID': userID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "PUT":
            # To update the details of the user
            pass

        elif input.method == "DELETE":
            # to delete the user
            pass

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/users/<userID>', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/users/<userID>/address', methods=["GET", "POST"])
def get_address_by_userID(userID):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = AddressResource.get_by_template({'ID': userID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "POST":
            data = input.data
            insert_id = AddressResource.add_by_template(data)
            # TODO use the method from the put object to update the addressID for the respective userID
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/users/<userID>/address', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/addresses', methods=["GET", "POST"])
def get_addresses():
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = AddressResource.get_by_template(None)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "POST":
            # userID must be present in the POST body,
            # otherwise there's no entry in the Users table
            data = input.data
            if 'userID' in data and data['userID']:
                userID = data['userID']
                del data['userID']
                insert_id = AddressResource.add_by_template(data)
                # TODO put method to update users table
                rsp = Response(json.dumps(insert_id, default=str), status=200, content_type="application/json")

            else:
                rsp = Response("POST body does not contain 'userID' field")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/addresses', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/address/<addressID>', methods=["GET", "PUT", "DELETE"])
def get_address_by_addressID(addressID):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = AddressResource.get_by_template({'ID': addressID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "PUT":
            # To update the details of the user
            pass

        elif input.method == "DELETE":
            # to delete the user
            pass

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/address/<addressID>', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/addresses/<addressID>/users', methods=["GET", "POST"])
def get_users_by_address(addressID):
    try:
        input = rest_utils.RESTContext(request)
        if input.method == "GET":
            res = UserResource.get_by_template({'addressID': addressID})
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        elif input.method == "POST":
            data = input.data
            data['addressID'] = addressID
            res = UserResource.add_by_template(data)
            rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

        else:
            rsp = Response("Method not implemented", status=501)

    except Exception as e:
        print(f"Path: '/addresses/<addressID>/users', Error: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>', methods=["GET", "POST"])
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = d_service.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)