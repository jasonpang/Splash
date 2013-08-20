from functools import wraps
import bcrypt
from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify
from models.user import User


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return _require_authentication()
        elif not _check_auth(auth.username, auth.password):
            return _incorrect_authentication()
        return f(*args, **kwargs)
    return decorated


def requires_super_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return _require_authentication()
        elif not _check_super_auth(auth.username, auth.password):
            return _incorrect_authentication()
        return f(*args, **kwargs)

    return decorated


def _require_authentication():
    message = {'message': "Authentication required."}
    resp = jsonify(message)
    resp.status_code = 401
    return resp


def _incorrect_authentication():
    message = {'message': "Authentication failed."}
    resp = jsonify(message)
    resp.status_code = 401
    return resp


def _check_auth(email, password):
    user = User.objects(email=email).first()
    input_password = bcrypt.hashpw(password, user.salt)
    if input_password == user.password:
        return True
    return False


def _check_super_auth(email, password):
    return email == "jasonpang2011@gmail.com" and password == "FV2Ogh4ZHP6rgrBEgHmyJMSJBoj9vvD5PX8Qs4xwoCO6es5R40z06cn3CHjF3Xz"

