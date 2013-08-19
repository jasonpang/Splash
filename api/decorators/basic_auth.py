from functools import wraps
from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="White"'
    return resp


def check_auth(username, password):
    return username == 'white' and password == 'splash'
