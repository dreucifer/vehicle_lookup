""" Vehicle Parts Lookup """

import json

from flask import Flask, redirect, url_for
from flask.ext.admin import Admin
import vehicle_lookup.database as db

app = Flask('vehicle_lookup')

app.debug = True
app.secret_key = "f3111bc8-8593-432b-9033-7db48e14685e"

admin = Admin(app)

import vehicle_lookup.views
