from flask import redirect, url_for, request
import flask.json as json
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
@app.route('/vl/')
def vl():
    callback = request.args.get('callback')
    make = request.args.get('make', None, type=str)
    model = request.args.get('model', None, type=str)
    year = request.args.get('year', None, type=str)
    engine = request.args.get('engine', None, type=str)

    if make:
        if model:
            if year:
                if engine:
                    return "unique vehicle GUID"
                else:
                    return "engine list"
            else:
                makes = Make.query.filter(Make.name == make).first()
                if makes:
                    models = Model.query.filter(Model.name == model).first()
                    if models in makes.models:
                        years = models.years
                        return "{0}({1})".format(callback, json.dumps([year.serialize for year in years]))
                return '{0}({1})'.format(callback, json.dumps([]))
        else:
            makes = Make.query.filter_by(name = make).first()
            if makes:
                models = Model.query.filter_by(make = makes).order_by(Model.name).all()
                return "{0}({1})".format(callback, json.dumps([line.serialize for line in models]))
            else:
                return "{0}({1})".format(callback, json.dumps([]))
    else:
        makes = Make.query.order_by(Make.name).all()
        return "{0}({1})".format(callback, json.dumps([make.serialize for make in makes]))

