#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, request


def valid_json(json):
    if not json:
        abort(400, 'Not a JSON')
    return json


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    states = storage.all(State)
    if request.method == 'POST':
        data = valid_json(request.get_json())
        if 'name' not in data.keys():
            abort(400, 'Missing name')
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201

    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state(state_id):
    s = storage.get(State, state_id)
    if s is None:
        abort(404)
    if request.method == 'PUT':
        data = valid_json(request.get_json())
        for key, value in data.items():
            if key not in ('id', 'updated_at', 'created_at'):
                setattr(s, key, value)
        storage.save()
        return jsonify(s.to_dict())
    elif request.method == 'DELETE':
        s.delete()
        storage.save()
        return jsonify({})
    else:
        return jsonify(s.to_dict())
