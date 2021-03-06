import os
from flask import Flask, Response, request, render_template, redirect, url_for, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
import json
import logging

from datetime import datetime

from middleware.service_helper import _get_service_by_name, _generate_user_links, \
    _generate_address_links, _generate_pages

import utils.rest_utils as rest_utils

from pprint import pprint

app = Flask(__name__)
CORS(app)

blueprint = make_google_blueprint(
    client_id=os.environ.get("OAUTH_ID", None),
    client_secret=os.environ.get("OAUTH_SECRET", None),
    scope=["profile", "email"],
    reprompt_consent=True
)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.register_blueprint(blueprint, url_prefix="/userlogin")

@app.route("/")
def index():
    return "Home"
    '''if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])'''


@app.route('/users', methods=["GET", "POST"])
def get_users():
    try:
        inputs = rest_utils.RESTContext(request)
        service = _get_service_by_name("user_service")
        if service is not None:
            if inputs.method == 'GET':
                res, total_count = service.find_by_template(inputs.args, inputs.fields, inputs.limit, inputs.offset)
                if res is not None:
                    res = _generate_user_links(res)
                    res = _generate_pages(res, inputs, total_count)
                    res = json.dumps(res, default = str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'POST':
                res = service.create(inputs.data)
                if res is not None:
                    values = list(map(str, res.values()))
                    key = "_".join(values)
                    headers = {"location": f"/users/{key}"}
                    rsp = Response("CREATED", status=201, content_type='text/plain', headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type='text/plain')

            else:
                rsp = Response("NOT IMPLEMENTED", status=501)
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /users\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/users/<userID>', methods=["GET", "PUT", "DELETE"])
def get_users_by_userID(userID):
    try:
        inputs= rest_utils.RESTContext(request)
        service = _get_service_by_name("user_service")
        if service is not None:
            if inputs.method == 'GET':
                args = {}
                if inputs.args:
                    args = inputs.args
                args['ID'] = userID

                res, total_count = service.find_by_template(args, inputs.fields) # single user (no limits/offset)
                if res is not None:
                    res = _generate_user_links(res)
                    res = _generate_pages(res, inputs, total_count) # single user
                    res = json.dumps(res, default = str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'PUT':
                res = service.update(userID, inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type='text/plain')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'DELETE':
                res = service.delete({"ID": userID})
                if res is not None:
                    rsp = Response(f"Rows Deleted: {res['no_of_rows_deleted']}", status=204, content_type='text/plain')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            else:
                rsp = Response("NOT IMPLEMENTED", status=501)

        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /users/<userID>\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/users/<userID>/address', methods=["GET", "POST"])
def get_address_by_userID(userID):
    try:
        inputs = rest_utils.RESTContext(request)
        service1 = _get_service_by_name("user_service")
        service2 = _get_service_by_name("address_service")

        if service1 is not None and service2 is not None:
            args = {}
            if inputs.args:
                args = inputs.args
            args['ID'] = userID
            res1, count1 = service1.find_by_template(args)
            # res1 = json.load(res1)
            if res1 is not None:
                if inputs.method == "GET":
                    address_id = res1[0].get('addressID', None)
                    if address_id is not None:
                        res2, count2 = service2.find_by_template({'ID': str(address_id)}, inputs.fields)
                        if res2 is not None:
                            res2 = _generate_address_links(res2, userID)
                            res2 = _generate_pages(res2, inputs, count2)
                            res2 = json.dumps(res2, default=str)
                            rsp = Response(res2, status=200, content_type='application/JSON')
                        else:
                            rsp = Response("NOT FOUND", status=404, content_type='text/plain')
                    else:
                        rsp = Response("No address associated with user", status=404, content_type='text/plain')

                elif inputs.method == "POST":
                    res = service2.create(inputs.data)
                    if res is not None:
                        values = list(map(str, res.values()))
                        key = "_".join(values)
                        headers = {"location": f"/users/{userID}/address/{key}"}
                        rsp = Response("CREATED", status=201, content_type='text/plain', headers=headers)

                        res2 = service1.update(userID, {'addressID': res['Insertion ID']})
                        rsp = Response("CREATED and UPDATED", status=201, content_type='text/plain', headers=headers)

                    else:
                        rsp = Response("NOT FOUND", status=404, content_type='text/plain')

                else:
                    rsp = Response("NOT IMPLEMENTED", status=501)

            else:
                rsp = Response("NOT FOUND", status=404, content_type='text/plain')
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /users/<userID>/address\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/addresses', methods=["GET", "POST"])
def get_addresses():
    try:
        inputs = rest_utils.RESTContext(request)
        service = _get_service_by_name("address_service")
        if service is not None:
            if inputs.method == "GET":
                res, count = service.find_by_template(inputs.args, inputs.fields, inputs.limit, inputs.offset)
                if res is not None:
                    res = _generate_address_links(res)
                    res = _generate_pages(res, inputs, count)
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'POST':
                res = service.create(inputs.data)
                if res is not None:
                    values = list(map(str, res.values()))
                    key = "_".join(values)
                    headers = {"location": f"/users/{key}"}
                    rsp = Response("CREATED", status=201, content_type='text/plain', headers=headers)

                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type='text/plain')

            else:
                rsp = Response("NOT IMPLEMENTED", status=501)
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /addresses\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/addresses/<addressID>', methods=["GET", "PUT", "DELETE"])
def get_address_by_addressID(addressID):
    try:
        inputs = rest_utils.RESTContext(request)
        service = _get_service_by_name("address_service")
        if service is not None:
            if inputs.method == 'GET':
                args = {}
                if inputs.args:
                    args = inputs.args
                args['ID'] = addressID

                res, count = service.find_by_template(args, inputs.fields)  # single address (no limits/offset)
                if res is not None:
                    res = _generate_address_links(res)
                    res = _generate_pages(res, inputs, count)
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'PUT':
                res = service.update(addressID, inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type='text/plain')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'DELETE':
                res = service.delete({"ID": addressID})
                if res is not None:
                    rsp = Response(f"Rows Deleted: {res['no_of_rows_deleted']}", status=204, content_type='text/plain')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            else:
                rsp = Response("NOT IMPLEMENTED", status=501)

        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /addresses/<addressID>\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/addresses/<addressID>/users', methods=["GET", "POST"])
def get_users_by_address(addressID):
    try:
        inputs = rest_utils.RESTContext(request)
        service = _get_service_by_name("user_service")
        if service is not None:
            if inputs.method == 'GET':
                res, count = service.find_by_template({'addressID': addressID}, inputs.fields, inputs.limit, inputs.offset)
                if res is not None:
                    res = _generate_user_links(res)
                    res = _generate_pages(res, inputs, count)
                    res = json.dumps(res, default = str)
                    rsp = Response(res, status=200, content_type='application/JSON')
                else:
                    rsp = Response("NOT FOUND", status=404, content_type='text/plain')

            elif inputs.method == 'POST':
                data = inputs.data
                data['addressID'] = addressID
                res = service.create(inputs.data)
                if res is not None:
                    values = list(map(str, res.values()))
                    key = "_".join(values)
                    headers = {"location": f"addresses/{addressID}/users/{key}"}
                    rsp = Response("CREATED", status=201, content_type='text/plain', headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type='text/plain')

            else:
                rsp = Response("NOT IMPLEMENTED", status=501)
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')

    except Exception as e:
        print(f"Path: /addresses/<addressID>/users\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)