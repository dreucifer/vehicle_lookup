import json
from flask import redirect, url_for
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from vehicle_lookup import app, admin
from vehicle_lookup.models import Make, Model, Year, Vehicle, Engine, Part
import vehicle_lookup.database as db

admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Part, db.session))
admin.add_view(ModelView(Make, db.session))
admin.add_view(ModelView(Model, db.session))
admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Engine, db.session))

class VehicleView(ModelView):
    def __init__(self, session, **kwargs):
        pass

@app.route('/')
def index():
    return "Hello, world"

@app.route('/vehicle/')
@app.route('/vl/', defaults={'make': None, 'model': None, 'year': None, 'engine': None})
@app.route('/vl/<make>/', defaults={'model': None, 'year': None, 'engine': None})
@app.route('/vl/<make>/<model>/', defaults={'year': None, 'engine': None})
@app.route('/vl/<make>/<model>/<int:year>/', defaults={'engine': None})
@app.route('/vl/<make>/<model>/<int:year>/<engine>')
def vl(*args, **kwargs):
    output = []
    if kwargs['make']:
        output.append('has make')
        if kwargs['model']:
            output.append('has model')
            if kwargs['year']:
                output.append('has year')
                if kwargs['engine']:
                    output.append('has engine')
                    return "unique vehicle GUID"
                else:
                    return "engine list"
            else:
                return "year list"
        else:
            return "model list"
    else:
        return "make list"

