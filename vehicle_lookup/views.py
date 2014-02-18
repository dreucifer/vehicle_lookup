from flask import redirect, url_for, request, render_template
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from vehicle_lookup import app, admin
from vehicle_lookup.models import Year, Make, Model, Engine, Config, Vehicle
import vehicle_lookup.database as db
import flask.json as json

class MyModelAdmin(ModelView):
    column_searchable_list = (Model.name,)
    inline_models = (Config,)

admin.add_view(ModelView(Year, db.session))
admin.add_view(ModelView(Make, db.session))
admin.add_view(MyModelAdmin(Model, db.session))
admin.add_view(ModelView(Engine, db.session))
admin.add_view(ModelView(Config, db.session))
admin.add_view(ModelView(Vehicle, db.session))

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
            configs = makes.models.filter_by(name = model).first().configs
            if year:
                year_obj = Year.query.filter_by(year = year).first()
                engines = configs.filter_by(year = year_obj).first().engines
                if engine:
                    return 'unique vehicle GUID'
                else:
                    status = 'Success'
                    data = [eng.serialize for eng in engines]
            else:
                status = 'Success'
                data = [config.serialize for config in configs.all()]
        else:
            status = 'Success'
            data = [line.serialize for line in models]
    else:
        makes = Make.query.order_by(Make.name).all()
        status = 'Success'
        data = [make.serialize for make in makes]
    return "{0}({1})".format(callback,
            json.dumps({ 'status': status, 'data': data }))

