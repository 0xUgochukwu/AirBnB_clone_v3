#!/usr/bin/python3
"""
view for User objects that handles all default RESTFul API actions
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """ API for Users """

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'email' not in body:
            abort(400, 'Missing email')
        if 'password' not in body:
            abort(400, 'Missing password')

        new_user = User(**body)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)

    else:
        u_list = storage.all(User)
        return jsonify([u.to_dict() for u in u_list.values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """ API for User """
    u = storage.get(User, user_id)
    if u is None:
        abort(404)

    if request.method == 'DELETE':
        u.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ('id', 'email', 'updated_at', 'created_at'):
                setattr(u, key, value)
        storage.save()
        return make_response(jsonify(u.to_dict()), 200)

    else:
        return jsonify(u.to_dict())
