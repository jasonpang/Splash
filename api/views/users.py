from flask import Flask, url_for
from flask import request
from flask import Response
from flask import json
from flask import jsonify
from decorators.basic_auth import check_auth, authenticate, requires_auth
import logging
import flask
from flask import Blueprint, render_template, abort
from decorators.requires_params import requires_params
import mongoengine
import pprint
from models.user import User

app = flask.current_app
users = Blueprint('users', __name__)


@users.route('/user/<userid>', methods=['GET'])
def get_user(userid):
    user = User.objects(id=userid).first()
    if not user is None:
        user_json = user.to_json()
        data = {
            'user': user_json,
        }
        resp = jsonify(data)
        return resp
    else:
        data = {
            'error': 'No user found with id \'' + userid + '\'.',
        }
        resp = jsonify(data)
        resp.status_code = 404
        return resp

@users.route('/users', methods = ['GET'])
def get_users():
    query = {}
    if 'name' in request.args:
        query['name'] = request.args['name']
    if 'phone' in request.args:
        query['phone'] = request.args['phone']
    if 'email' in request.args:
        query['email'] = request.args['email']
    users = User.objects(**query)
    data = {
        'users': json.loads(users.to_json()),
    }
    js = json.dumps(data)
    resp = Response(js, status = 200, mimetype = 'application/json')
    return resp


@users.route('/user', methods = ['POST'])
@requires_params(['name', 'phone', 'email', 'quote', 'school', 'year', 'major', 'company', 'title', 'location', 'interests', 'skills', 'profile', 'contacts'])
def create_user():
    user = User(
        name=request.json['name'],
        phone=request.json['phone'],
        email=request.json['email'],
        picture_profile='data:image/gif;base64,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',
        picture_thumbnail='data:image/gif;base64,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',
        quote=request.json['quote'],
        school=request.json['school'],
        year=request.json['year'],
        major=request.json['major'],
        company=request.json['company'],
        title=request.json['title'],
        location=request.json['location'],
        interests=request.json['interests'],
        skills=request.json['skills'],
        profile=request.json['profile'],
        contacts=request.json['contacts'],
    )
    user.save()
    app.logger.info('Created \'' + str(user.name) + '\'.')
    return Response(status=200, mimetype='application/json')


@users.route('/user/<userid>', methods = ['PUT'])
def update_user(userid):
    if not userid:
        return Response(status=400, mimetype='application/json')
    json = request.get_json(force = True)
    user = User.objects(id=userid).first()
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


@users.route('/user/<userid>', methods=['DELETE'])
def delete_user(userid):
    user = User.objects(id=userid).first()
    if not user is None:
        user.delete()
        return Response(status = 200, mimetype = 'application/json')
    else:
        data = {
            'error': 'No user found with id \'' + userid + '\'.',
        }
        resp = jsonify(data)
        resp.status_code = 404
        return resp


@users.route('/users', methods = ['DELETE'])
def delete_all_users():
    for user in User.objects:
        user.delete()
    return Response(status = 200, mimetype = 'application/json')