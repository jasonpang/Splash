from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify
from decorators.basic_auth import requires_auth, requires_super_auth
import logging
import flask
from flask import Blueprint, render_template, abort
from decorators.requires_params import requires_params
import mongoengine
import pprint
from models.user import User

app = flask.current_app
users = Blueprint('users', __name__)


@users.route('/user', methods = ['GET'])
@requires_auth
def get_user():
    user = User.objects(email = request.authorization.username).first()
    if not user is None:
        user_json = user.to_json()
        data = {
            'user': user_json,
        }
        resp = jsonify(data)
        return resp
    else:
        data = {
            'error': 'No user found with email \'' + request.authorization.username + '\'.',
        }
        resp = jsonify(data)
        resp.status_code = 404
        return resp


@users.route('/user', methods = ['PUT'])
@requires_auth
def update_user():
    user = User.objects(email = request.authorization.username).first()
    json = request.get_json(force = True)
    if 'name' in request.json:
        user.name = request.json['name']
    if 'phone' in request.json:
        user.phone = request.json['phone']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'picture_profile' in request.json:
        user.picture_profile = request.json['picture_profile']
    if 'picture_thumbnail' in request.json:
        user.picture_thumbnail = request.json['picture_thumbnail']
    if 'quote' in request.json:
        user.quote = request.json['quote']
    if 'school' in request.json:
        user.school = request.json['school']
    if 'year' in request.json:
        user.year = request.json['year']
    if 'major' in request.json:
        user.major = request.json['major']
    if 'company' in request.json:
        user.company = request.json['company']
    if 'title' in request.json:
        user.title = request.json['title']
    if 'location' in request.json:
        user.location = request.json['location']
    if 'interests' in request.json:
        user.interests = request.json['interests']
    if 'skills' in request.json:
        user.skills = request.json['skills']
    if 'profile' in request.json:
        user.profile = request.json['profile']
    if 'contacts' in request.json:
        user.contacts = request.json['contacts']
    user.save()
    app.logger.info('Updated \'' + str(user.name) + '\'.')
    return Response(status = 200, mimetype = 'application/json')


@users.route('/user', methods=['DELETE'])
@requires_auth
def delete_user():
    user = User.objects(email = request.authorization.username).first()
    if not user is None:
        user.delete()
        return Response(status = 200, mimetype = 'application/json')
    else:
        data = {
            'error': 'No user found with email \'' + request.authorization.username + '\'.',
        }
        resp = jsonify(data)
        resp.status_code = 404
        return resp


@users.route('/users', methods = ['DELETE'])
@requires_super_auth
def delete_all_users():
    for user in User.objects:
        user.delete()
    return Response(status = 200, mimetype = 'application/json')