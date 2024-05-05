#!/usr/bin/python3
"""new flask blueprint
and import modules for all the tasks
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
