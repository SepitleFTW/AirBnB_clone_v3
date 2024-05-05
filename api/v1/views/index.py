#!/usr/bin/python3
"""
this if for flask app; app views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/ap1/v1/stats')
def api_status():
    """
    api statsus
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
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
