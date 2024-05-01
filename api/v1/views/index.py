#!/usr/bin/python3
"""
flask app; app views
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status/')
def api_status():
    """
    api statsus
    """
    response = {'status': "OK"}
    return jsonify(response)

