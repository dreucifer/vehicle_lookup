from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField

class VehicleView(ModelView):
    def __init__(self, session, **kwargs):
        pass
