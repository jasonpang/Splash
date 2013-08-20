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
    user = User.objects(email = request.authorization.username).exclude('password').exclude('salt').exclude('id').exclude('contacts').first()
    user_json = json.loads(user.to_json())
    data = {
        'user': user_json,
    }
    return Response(json.dumps(data), status = 200, mimetype = 'application/json')


@users.route('/user/<userid>', methods = ['GET'])
@requires_auth
def get_user_by_id(userid):
    users = User.objects(id = userid).exclude('password').exclude('salt').exclude(
        'id').exclude('contacts')
    if len(users) > 0:
        user = users.first()
        user_json = json.loads(user.to_json())
        data = {
            'user': user_json,
        }
        return Response(json.dumps(data), status = 200, mimetype = 'application/json')
    else:
        data = {
            'user': 'No user with that id exists.',
        }
        return Response(json.dumps(data), status = 404, mimetype = 'application/json')


@users.route('/user/contacts', methods = ['GET'])
@requires_auth
def get_user_contacts():
    user = User.objects(email = request.authorization.username).first()
    user_json = json.loads(user.to_json())
    user_contacts = user_json['contacts'] # Is a list of dictionaries, each entry is a contact
    contacts = []
    for contact in user_contacts:
        contacts.append(contact.values()[0]) # Get the value id only

    data = {
        'contacts': contacts,
    }
    return Response(json.dumps(data), status = 200, mimetype = 'application/json')


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
    if 'password' in request.json:
        user.password = request.json['password']
    if 'description' in request.json:
        user.description = request.json['description']
    if 'education' in request.json:
        user.education = request.json['education']
    if 'employer' in request.json:
        user.employer = request.json['employer']
    if 'skills' in request.json:
        user.skills = request.json['skills']
    if 'interests' in request.json:
        user.interests = request.json['interests']
    user.save()
    return Response(status = 200, mimetype = 'application/json')


@users.route('/user/contact', methods = ['PUT'])
@requires_auth
@requires_params(['contact_email'])
def add_user_contact():
    user = User.objects(email = request.authorization.username).first()
    contacts_with_email = User.objects(email = request.json['contact_email'])
    if len(contacts_with_email) > 0:
        contact = contacts_with_email.first()
        if contact not in user.contacts:
            user.contacts.append(contact)
            user.save()
            return Response(status = 200, mimetype = 'application/json')
        else:
            data = {
                'message': 'This user already has that contact added.'
            }
            return Response(json.dumps(data), status = 400, mimetype = 'application/json')
    else:
        data = {
            'message': 'The contact does not exist.'
        }
        return Response(json.dumps(data), status = 404, mimetype = 'application/json')


@users.route('/user/contact', methods = ['DELETE'])
@requires_auth
@requires_params(['contact_email'])
def remove_user_contact():
    user = User.objects(email = request.authorization.username).first()
    contacts_with_email = User.objects(email = request.args['contact_email'])
    if len(contacts_with_email) > 0:
        contact = contacts_with_email.first()
        if contact in user.contacts:
            user.contacts.remove(contact)
            user.save()
            return Response(status = 200, mimetype = 'application/json')
        else:
            data = {
                'message': 'This user does not have that contact added.'
            }
            return Response(json.dumps(data), status = 400, mimetype = 'application/json')
    else:
        data = {
            'message': 'The contact does not exist.'
        }
        return Response(json.dumps(data), status = 400, mimetype = 'application/json')


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
        return Response(json.dumps(data), status = 404, mimetype = 'application/json')


@users.route('/users', methods = ['DELETE'])
@requires_super_auth
def delete_all_users():
    for user in User.objects:
        user.delete()
    return Response(status = 200, mimetype = 'application/json')