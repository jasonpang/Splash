from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from mongoengine import connect
import logging


def configure_app(name):
    app = Flask(name)
    configure_logging(app)
    return_errors_as_json(app)
    configure_db(app)
    return app


def configure_logging(app):
    file_handler = logging.FileHandler('logs/app.log')
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(funcName)s:%(lineno)d):  \033[37m%(message)s\033[0m')
    formatter.datefmt = '[%A, %B%e %Y %l:%M:%S %p]'
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


def configure_db(app):
    connect('white')


# http://flask.pocoo.org/snippets/83/
def return_errors_as_json(app):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response
    
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error        
    return app

