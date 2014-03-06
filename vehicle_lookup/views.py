""" This holds the view logic and URL information """
from flask import redirect, url_for, request, render_template
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from vehicle_lookup import app, admin
from vehicle_lookup.models import Year, Part, Make, Model, Engine, Type
from vehicle_lookup.helpers import (
        get_or_create, get_makes, get_types,
        get_models, get_years, get_engines)
import vehicle_lookup.database as db
import flask.json as json

class MyModelAdmin(ModelView):
    column_searchable_list = (Model.name,)

class MyPartAdmin(ModelView):
    column_searchable_list = (Part.name,)
    column_list = ('name', 'desc_short')

admin.add_view(ModelView(Make, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(MyModelAdmin(Model, db.session))
admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Engine, db.session))
admin.add_view(MyPartAdmin(Part, db.session))

@app.route('/')
def index():
    """ Render the basic template """
    app.logger.info('test')
    return render_template('index.html')

@app.route('/vehicle', methods=['POST','GET'])
@app.route('/vl', methods=['POST','GET'])
def vl():
    status = 'Failure'
    data = []

    make = request.values.get('make', None, type=str)
    vtype = request.values.get('type', None, type=str)
    model = request.values.get('model', None, type=str)
    year = request.values.get('year', None, type=str)
    engine = request.values.get('engine', None, type=str)

    if make:
        if vtype:
            data.append('crumps')
        else:
            data = data + list(get_types(make))
    else:
        data = data + list(get_makes())

    return json.dumps({ 'status': status, 'data': data })

@app.route('/vlmake', methods=['POST', 'GET'])
def vlmake():
    status = 'Success'
    data = list(get_makes())
    return json.dumps({ 'status': status, 'data': data })

@app.route('/vltype', methods=['POST', 'GET'])
def vltype():
    make = request.values.get('make', None, type=int)
    data = []
    if make:
        status = 'Success'
        data = list(get_types(make))
    else:
        status = 'Failure'
    return json.dumps({ 'status': status, 'data': data })

@app.route('/vlmodel', methods=['POST', 'GET'])
def vlmodel():
    data = []
    make = request.values.get('make', None, type=int)
    vtype = request.values.get('type', None, type=str)
    if make and vtype:
        status = 'Success'
        data = list(get_models(make, vtype))
    else:
        status = 'Failure'
    return json.dumps({'status': status, 'data': data})

@app.route('/vlyear', methods=['POST', 'GET'])
def vlyear():
    data = []
    model = request.values.get('model', None, type=int)
    if model:
        status = 'Success'
        data = list(get_years(model))
    else:
        status = 'Failure'

    return json.dumps({'status': status, 'data': data})

@app.route('/parts')
@app.route('/pt')
def get_parts():
    from uuid import UUID
    callback = request.args.get('callback')
    status = 'Failure'
    data = []
    vehicle_guid = request.args.get('guid')

    vehicle = Vehicle.query.filter_by(guid = UUID(vehicle_guid)).first()
    if vehicle:
        parts = vehicle.parts.all()
        if parts:
            status = 'Success'
            data = [part.serialize for part in vehicle.parts.all()]

    return "{0}({1})".format(callback,
            json.dumps({ 'status': status, 'data': data }))
