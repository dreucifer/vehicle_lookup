from flask import redirect, url_for, request, render_template
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from vehicle_lookup import app, admin
from vehicle_lookup.models import Year, Make, Model, Engine, Config
import vehicle_lookup.database as db
import flask.json as json

admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Make, db.session))
admin.add_view(ModelView(Model, db.session))
admin.add_view(ModelView(Engine, db.session))
admin.add_view(ModelView(Config, db.session))

class VehicleView(ModelView):
    def __init__(self, session, **kwargs):
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicle/')
@app.route('/vl/')
def vl():
    callback = request.args.get('callback')
    status = 'Failure'
    data = []
    make = request.args.get('make', None, type=str)
    model = request.args.get('model', None, type=str)
    year = request.args.get('year', None, type=str)
    engine = request.args.get('engine', None, type=str)

    if make:
        makes = Make.query.filter_by(name = make).first()
        models = makes.models.order_by(Model.name).all()

        if model:
            if year:
                if engine:
                    return 'unique vehicle GUID'
                else:
                    return 'engine list'
            else:

                years = makes.models.filter_by(name = model).first().years
                status = 'Success'
                data = [year.serialize for year in years]
        else:
            status = 'Success'
            data = [line.serialize for line in models]
    else:
        makes = Make.query.order_by(Make.name).all()
        status = 'Success'
        data = [make.serialize for make in makes]
    return "{0}({1})".format(callback,
            json.dumps({ 'status': status, 'data': data }))

