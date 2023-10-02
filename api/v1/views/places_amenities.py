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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def alter_place_amenities(place_id, amenity_id):
    """ Deletes or Creates an amenity """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    db = storage.__class__.__name__
    if db == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        if amenity.to_dict() not in amenities:
            abort(404)
        if db == 'DBStorage':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity.id)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        if amenity.to_dict() in amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        if db == 'DBStorage':
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity.id)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    """ Retrieves amenities for a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    db = storage.__class__.__name__
    if db == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)
