#!/usr/bin/python3
"""
API endpoints for managing amenities
"""
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieve all amenities"""
    amenity_list = [amenity.to_dict() for amenity in
                    storage.all(Amenity).values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a specific amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return abort(400, 'Invalid JSON data')
    if not data or 'name' not in data:
        return abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an existing amenity"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return abort(400, 'Not a JSON')
    if not data:
        return abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
