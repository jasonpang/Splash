from flask import request
from flask import Response
from flask import jsonify
import flask
from flask import Blueprint
import os

app = flask.current_app
server = Blueprint('server', __name__)


@server.route('/', methods=['GET'])
def server_default():
    response = Response(status=200, mimetype='application/json')
    return response


@server.route('/logs', methods=['DELETE'])
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
            response = jsonify(data)
        else:
            data = {
                'message': 'There are no server logs.',
            }
            response = jsonify(data)
    except Exception:
        app.logger.error("Could not delete server logs." + str(Exception))
        data = {
            'message': 'Could not delete server logs.',
        }
        response = jsonify(data)
        response.status = 500
    return response
