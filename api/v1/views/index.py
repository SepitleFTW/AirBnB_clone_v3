#!/usr/bin/python3
"""
flask app; app views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
<<<<<<< HEAD
=======


>>>>>>> 4db62a97956c1b98b02897d831e662dd8282c6ea

@app_views.route('/status/')
def api_status():
    """
    api statsus
    """
    response = {'status': "OK"}
    return jsonify(response)


@app_views.route('/stats')
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
