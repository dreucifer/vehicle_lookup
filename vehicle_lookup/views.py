from flask import redirect, url_for, request, render_template
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from vehicle_lookup import app, admin
from vehicle_lookup.models import Year, Part, Make, Model, Engine, Config, Vehicle, get_or_create
import vehicle_lookup.database as db
import flask.json as json

class MyModelAdmin(ModelView):
    column_searchable_list = (Model.name,)
    inline_models = (Config,)

class MyPartAdmin(ModelView):
    column_searchable_list = (Part.name,)
    column_list = ('name', 'desc_short')

admin.add_view(ModelView(Make, db.session))
admin.add_view(MyModelAdmin(Model, db.session))
admin.add_view(ModelView(Engine, db.session))
admin.add_view(ModelView(Config, db.session))
admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(MyPartAdmin(Part, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicle/', methods=['POST','GET'])
@app.route('/vl/', methods=['POST','GET'])
def vl():
    status = 'Failure'
    data = []
    make = request.values.get('make', None, type=str)
    model = request.values.get('model', None, type=str)
    year = request.values.get('year', None, type=str)
    engine = request.values.get('engine', None, type=str)

    if make:
        makes = Make.query.filter_by(name = make).first()
        models = makes.models.order_by(Model.name).all()
        if model:
            configs = makes.models.filter_by(name = model).first().configs
            if year:
                year_obj = Year.query.filter_by(year = year).first()
                engines = configs.filter_by(year = year_obj).first().engines
                if engine:
                    vehicle = get_or_create(db.session, Vehicle,
                            year = year_obj,
                            make = get_or_create(db.session, Make, name = make),
                            model = get_or_create(db.session, Model, name = model),
                            engine = get_or_create(db.session, Engine, name = engine))
                    status = 'Success'
                    data = [vehicle.guid]
                else:
                    status = 'Success'
                    data = [eng.serialize for eng in engines]
            else:
                status = 'Success'
                data = sorted([config.serialize for config in configs.all()])
        else:
            status = 'Success'
            data = sorted([line.serialize for line in models])
    else:
        makes = Make.query.order_by(Make.name).all()
        status = 'Success'
        data = sorted([make.serialize for make in makes])
    return json.dumps({ 'status': status, 'data': data })

def get_makes():
    pass

def get_types(make):
    pass

def get_models(make, vehicle_type):
    pass

def get_years(make, vehicle_type, model):
    pass

def get_engines(make, vehicle_type, model, year):
    pass

def get_vehicle(make, vehicle_type, model, year, engine):
    pass


@app.route('/parts/')
@app.route('/pt/')
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
