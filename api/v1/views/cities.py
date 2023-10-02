#!/usr/bin/python3
"""
view for City objects that handles all default RESTFul API actions
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city_api(city_id):
    """ API for City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({})
    elif request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')

        ignore = ['id', 'created_at', 'updated_at', 'state_id']
        for key, value in body.items():
            if key not in ignore:
                setattr(city, key, value)

        storage.save()
        return make_response(jsonify(city.to_dict()), 200)

    else:
        return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def state_cities(state_id):
    """ API for cities in a state """
    s = storage.get(State, state_id)
    if s is None:
        abort(404)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'name' not in body:
            abort(400, 'Missing name')

        new_city = City(**body)
        setattr(new_city, 'state_id', state_id)
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)

    else:
        return jsonify([city.to_dict() for city in s.cities])
