#!/usr/bin/python3
"""
view for Reviews objects that handles all default RESTFul API actions
"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def places(review_id):
    """ Retrieves, Deletes and Updates the details of a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')

        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        return jsonify(review.to_dict)


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    """ Retrieves and creates reviews for a place """
    place = storage.get(Place, place_id)
    if place is None:
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
        if 'text' not in body:
            abort(400, 'Missing text')

        new_review = Review(**body)
        setattr(new_review, 'place_id', place_id)
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)

    else:
        return jsonify([review.to_dict() for review in place.reviews])
