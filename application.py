#!/bin/env python
""" Vehicle Parts Lookup """

import json

from flask import Flask, redirect, url_for
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from models import Make, Model, Year, Vehicle, Engine, Part
import database as db

app = Flask("vl")
app.debug = True

admin = Admin(app)
admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Part, db.session))
admin.add_view(ModelView(Make, db.session))
admin.add_view(ModelView(Model, db.session))
admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Engine, db.session))

@app.route('/')
def index():
    return "Hello, world"

@app.route('/vehicle/')
@app.route('/vl/', defaults={'make': None, 'model': None, 'year': None})
@app.route('/vl/<make>/', defaults={'model': None, 'year': None})
@app.route('/vl/<make>/<model>/', defaults={'year': None})
@app.route('/vl/<make>/<model>/<int:year>/')
def vl(*args, **kwargs):
    output = []
    if kwargs['make']:
        output.append('has make')
        if kwargs['model']:
            output.append('has model')
            if kwargs['year']:
                output.append('has year')
            else:
                return "year list"
        else:
            return "model list"
    else:
        return "make list"

app.secret_key = "f3111bc8-8593-432b-9033-7db48e14685e"

if __name__ == '__main__':
    app.run()
