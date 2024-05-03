from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404, 'User not found')

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
