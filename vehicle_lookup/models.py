import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
import database as db
from custom_types import GUID

class Make(db.Base):
    __tablename__ = 'makes'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    models = relationship("Model", backref='make', lazy='dynamic')

    def __unicode__(self):
        return "%s" % self.name
    
    def __repr__(self):
        return "<Make(name='%s')>" % self.name

    @property
    def serialize(self):
        return self.name


class Model(db.Base):
    __tablename__ = 'models'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    make_id = Column(Integer, ForeignKey('makes.id_'))
    configs = relationship("Config", backref="model", lazy='dynamic')
    
    def __unicode__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return "<Model(name='%s', make='%s')>" % (
                self.name, self.make.name)

    @property
    def serialize(self):
        return self.name


class Year(db.Base):
    __tablename__ = 'years'

    id_ = Column(Integer, primary_key=True)
    year = Column(Integer)

    def __unicode__(self):
        return "%s" % self.year

    def __repr__(self):
        return "<Year(%s)>" % self.year

    @property
    def serialize(self):
        return dict('year', self.year)


config_engines = Table("config_engines", db.Base.metadata,
        Column("config_id",
            Integer,
            ForeignKey("configs.id_"), primary_key=True),
        Column("engine_id",
            Integer,
            ForeignKey("engines.id_"), primary_key=True))


class Config(db.Base):
    __tablename__ = 'configs'
    id_ = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey("years.year"))
    model_id = Column(Integer, ForeignKey("models.id_"))
    year = relationship("Year", uselist=False)
    engines = relationship("Engine", secondary=config_engines)

    def __unicode__(self):
        return "%s" % self.year.year

    @property
    def serialize(self):
        return self.year.year


class Engine(db.Base):
    __tablename__ = 'engines'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    config = Column(String)
    cylinders = Column(Integer)
    size_liter = Column(String)
    size_cid = Column(Integer)

    def __unicode__(self):
        return "%s" % self.name

    @property
    def serialize(self):
        return self.name


class Vehicle(db.Base):
    __tablename__ = 'vehicles'

    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    year_id = Column(Integer, ForeignKey('years.id_'))
    make_id = Column(Integer, ForeignKey('makes.id_'))
    model_id = Column(Integer, ForeignKey('models.id_'))
    engine_id = Column(Integer, ForeignKey('engines.id_'))
    year = relationship("Year", uselist=False)
    make = relationship("Make", uselist=False)
    model = relationship("Model", uselist=False)
    engine = relationship("Engine", uselist=False)

    def __unicode__(self):
        return "%d %s %s %s" % (
                self.year.year,
                self.make.name,
                self.model.name,
                self.engine.name
            )

    def __repr__(self):
        return "<Vehicle(guid=%r)>" % (self.guid)


vehicle_parts = Table('vehicle_parts', db.Base.metadata,
        Column('vehicle_guid', GUID(), ForeignKey('vehicles.guid')),
        Column('part_guid', GUID(), ForeignKey('parts.guid')))


class Part(db.Base):
    __tablename__ = 'parts'

    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    desc_short = Column(String)
    desc_long = Column(Text)

def get_or_create_year(session, year):
    result = Year.query.filter_by(year = year).first()
    if result:
        return result
    else:
        result = Year(year = year)
        session.add(result)
        return result

def get_or_create_make(session, make):
    result = Make.query.filter_by(name = make).first()
    if result:
        return result
    else:
        result = Make(name = make)
        session.add(result)
        return result

def get_or_create_model(session, model):
    result = Model.query.filter_by(name = model).first()
    if result:
        return result
    else:
        result = Model(name = model)
        session.add(result)
        return result

def get_or_create_config(session, model):
    result = Model.query.filter_by(name = model).first()
    if result:
        return result
    else:
        result = Model(name = model)
        session.add(result)
        return result

def get_or_create_vehicle(session, **kwargs):
    result = Vehicle.query.filter_by(**kwargs).first()
    if not result:
        result = Vehicle(**kwargs)
        session.add(result)
    return result

def import_data(data_filename):
    import codecs
    from csv import reader
    with open(data_filename) as data_file:
        data_reader = reader(data_file, delimiter=",")
        for row in data_reader:
            year, make, model = row
            year = get_or_create_year(db.session, int(year.decode('ascii', 'ignore')))
            make = get_or_create_make(db.session, make.decode('ascii', 'ignore'))
            model = get_or_create_model(db.session, model.decode('ascii', 'ignore'))
            make.models.append(model)
            model.configs.append(Config(year = year))
            db.session.commit()
            print ", ".join([str(year.year), make.name, model.name])

def generate_vehicles():
    for make in Make.query.all():
        print make.name
        for model in make.models:
            print "\t" + model.name
            for config in model.configs.all():
                print "\t\t" + str(config.year.year)
                for engine in config.engines:
                    print "\t\t\t" + engine.name
                    vehicle = get_or_create_vehicle(
                            db.session,
                            year = config.year,
                            make = make,
                            model = model,
                            engine = engine)
                    if vehicle:
                        print "\t\t\t" + vehicle.__unicode__()
    db.session.commit()
