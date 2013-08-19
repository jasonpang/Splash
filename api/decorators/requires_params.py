from functools import wraps
import pprint
from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify

def requires_params(*params):
    no_args = False
    if len(params) == 1 and callable(params[0]):
        # We were called without args
        func = params[0]
        no_args = True

    def outer(func):
        @wraps(func)
        def function(*actual_params):
            if len(params) > 0:
                missing_params = _get_missing_params(*params)
                if len(missing_params) > 0:
                    error = {'error': 'Missing parameters: ' + ', '.join(missing_params)}
                    resp = jsonify(error)
                    resp.status_code = 400
                    return resp
                else:
                    return func(*actual_params)
            else:
                return func(*actual_params)
        return function

    if no_args:
        return outer(func)
    else:
        return outer

def _get_missing_params(params):
    missing_params = []
    if request.method == 'GET' or request.method == 'DELETE':
        for param in params:
            if not param in request.args:
                missing_params.append(param)
    elif request.method == 'PUT' or request.method == 'POST':
        json = request.get_json(force=True)
        if not json is False:
            for param in params:
                if not param in json:
                    missing_params.append(param)
    return missing_params