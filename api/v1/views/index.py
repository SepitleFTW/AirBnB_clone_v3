#!/usr/bin/python3
"""
flask app; app views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/stats/')
def api_status():
    """
    api statsus
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/api/v1/stats')
def get_status():
    """gets the status
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }

    return jsonify(stats)
