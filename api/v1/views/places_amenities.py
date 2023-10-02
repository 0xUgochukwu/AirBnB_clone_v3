#!/usr/bin/python3
"""
view for Reviews objects that handles all default RESTFul API actions
"""
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
    amenities = place_amenities(place_id)
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None or
    amenity not in amenities and request.method == 'DELETE':
        abort(404)

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else request.method == 'POST':
        if amenity in amenities:
            return jsonify(amenity.to_dict())
        place.amenities(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    """ Retrieves amenities for a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])
