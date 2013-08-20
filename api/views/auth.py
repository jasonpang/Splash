from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify
from decorators.basic_auth import requires_auth
import logging
import flask
from flask import Blueprint, render_template, abort
from decorators.requires_params import requires_params
import mongoengine
import pprint
from models.user import User
import bcrypt

app = flask.current_app
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
@requires_params(['email', 'password'])
def auth_signup():
    email = request.json['email']
    password = request.json['password']

    users_with_email = User.objects(email=email)
    if len(users_with_email) > 0:
        data = {
            'message': 'An account with that email already exists.',
        }
        return Response(json.dumps(data), status = 400, mimetype = 'application/json')
    else:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password, salt)
        user = User(
            email = email,
            password = password,
            salt = salt
        )
        user.save()
        return Response(status = 200, mimetype = 'application/json')


@auth.route('/login', methods = ['POST'])
@requires_auth
def auth_login():
    return Response(status = 200, mimetype = 'application/json')