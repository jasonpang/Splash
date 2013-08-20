import json
from flask import request
from flask import Response
from flask import jsonify
import flask
from flask import Blueprint
import os
from decorators.basic_auth import requires_super_auth

app = flask.current_app
server = Blueprint('server', __name__)


@server.route('/', methods=['GET'])
def server_default():
    response = Response(status=200, mimetype='application/json')
    return response


@server.route('/logs', methods=['DELETE'])
@requires_super_auth
def server_clear_logs():
    file_path = 'logs/app.log'
    try:
        exists = os.path.exists(file_path)
        if exists:
            os.remove(file_path)
            app.logger.info("\'" + request.remote_addr + "\' deleted server logs.")
            data = {
                'message': 'Server logs have been deleted.',
            }
            return Response(json.dumps(data), status = 200, mimetype = 'application/json')
        else:
            data = {
                'message': 'There are no server logs.',
            }
            return Response(json.dumps(data), status = 500, mimetype = 'application/json')
    except Exception:
        app.logger.error("Could not delete server logs." + str(Exception))
        data = {
            'message': 'Could not delete server logs.',
        }
        return Response(json.dumps(data), status = 500, mimetype = 'application/json')
