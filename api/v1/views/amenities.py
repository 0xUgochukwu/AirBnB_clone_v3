#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """ API for Ameities """

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'name' not in body:
            abort(400, 'Missing name')

        new_a = Amenity(**body)
        storage.new(new_a)
        storage.save()
        return make_response(jsonify(new_a.to_dict()), 201)

    else:
        a_list = storage.all(Amenity)
        return jsonify([a.to_dict() for a in a_list.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """ API for Amenity """
    a = storage.get(Amenity, amenity_id)
    if a is None:
        abort(404)

    if request.method == 'DELETE':
        a.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if not body['name']:
            abort(400, 'Missing name')

        for key, value in body.items():
            setattr(a, key, value)

        storage.save()
        return make_response(jsonify(a.to_dict()), 200)

    else:
        return jsonify(a.to_dict())
