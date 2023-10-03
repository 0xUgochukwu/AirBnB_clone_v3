#!/usr/bin/python3
"""
view for Place objects that handles all default RESTFul API actions
"""
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews(place_id):
    """ Retrieves, Deletes and Updates the details of a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')

        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    else:
        return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_places(city_id):
    """ Retrieves places in a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'user_id' not in body:
            abort(400, 'Missing user_id')
        user = storage.get(User, body['user_id'])
        if user is None:
            abort(404)
        if 'name' not in body:
            abort(400, 'Missing name')

        new_place = Place(**body)
        setattr(new_place, 'city_id', city_id)
        storage.new(new_place)
        storage.save()
        return make_response(jsonify(new_place.to_dict()), 201)

    else:
        return jsonify([place.to_dict() for place in city.places])

def add_place(place, arr, amenities):
    if place in arr:
        return
    if len(amenities) != 0:
        for amenity_id in amenities:
            amenity = storage.get(Amenity, amenity_id)
            if amenity.to_dict() in place.amenities:
                if place.to_dict() not in arr:
                    arr.append(place.to_dict())
    else:
        if place.to_dict() not in arr:
            arr.append(place.to_dict())

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        Retrieves places depending on the JSON in the body of the request
    """
    body = request.get_json()
    result = []

    if not body:
        abort(400, 'Not a JSON')

    amenities = body['amenities'] if 'amenities' in body else []
    if len(body) == 0 or (('states' not in body.keys() or len(body['states']) == 0)
                            and ('cities' not in body.keys()) or len(body['cities']) == 0):
        if 'amenities' in body and len(amenities) != 0:
            for place in storage.all(Place):
                add_place(place, result, amenities)
            return jsonify(result)
        else:
            return jsonify([p.to_dict() for p in storage.all(Place).values()])

    if 'states' in body:
        for state_id in body['states']:
            state = storage.get(State, state_id)
            for city in state.cities:
                for place in city.places:
                    add_place(place, result, amenities)

    if 'cities' in body:
        for city_id in body['cities']:
            city = storage.get(City, city_id)
            for place in city.places:
                add_place(place, result, amenities)
    
    return jsonify(result)
