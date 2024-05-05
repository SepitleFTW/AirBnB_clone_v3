#!/usr/bin/python3
from flask import jsonify, abort, request
from models import app, City, State


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in City.filter(state_id=state_id)]
    return jsonify(cities)


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200


@app.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    city = City(**data, state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    # Ignore keys: id, state_id, created_at, and updated_at
    for key in ['id', 'state_id', 'created_at', 'updated_at']:
        data.pop(key, None)
    city.update(**data)
    return jsonify(city.to_dict()), 200
