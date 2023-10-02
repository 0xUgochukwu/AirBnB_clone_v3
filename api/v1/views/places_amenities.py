#!/usr/bin/python3
"""
view for Reviews objects that handles all default RESTFul API actions
"""
import json
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def alter_place_amenities(place_id, amenity_id):
    """ Deletes or Creates an amenity """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    amenity = storage.get(Amenity, amenity_id)
    db = storage.__class__.__name__

    if amenity is None or\
            amenity not in amenities and request.method == 'DELETE':
        abort(404)

    if request.method == 'DELETE':
        if db == 'DBStorage':
            place.amenities.remove(amenity)
        else:
            amenity_ids.remove(amenity.id)
        return make_response(jsonify({}), 200)
    else:
        if amenity in amenities:
            return jsonify(amenity.to_dict())
        if db == 'DBStorage':
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity.id)
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    """ Retrieves amenities for a place """
    print(storage.__class__.__name__)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])
