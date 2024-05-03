#!/usr/bin/python3
"""
place reviews for the reviews module and
class
"""
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by ID"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a new Review"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
