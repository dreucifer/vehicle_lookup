import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
import database as db
from custom_types import GUID

class Make(db.Base):
    __tablename__ = 'makes'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    types = relationship('Type', backref='make', lazy='dynamic')

    def __unicode__(self):
        return "%s" % self.name
    
    def __repr__(self):
        return "<Make(name='%s')>" % self.name

    @property
    def serialize(self):
        return self.name


class Type(db.Base):
    __tablename__ = 'types'

    id_ = Column(Integer, primary_key=True)
    make_id = Column(Integer, ForeignKey('makes.id_'))
    name = Column(String)
    models = relationship('Model', backref='type', lazy='dynamic')

model_years = Table('model_years', db.Base.metadata)

class Model(db.Base):
    __tablename__ = 'models'

    id_ = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id_'))
    name = Column(String)
    years = relationship('Year',
            backref='model',
            lazy='dynamic',
            secondary=model_years)
    
    def __unicode__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return "<Model>"

    @property
    def serialize(self):
        return self.name


class Year(db.Base):
    __tablename__ = 'years'

    id_ = Column(Integer, primary_key=True)
    year = Column(String)

    def __unicode__(self):
        return "%s" % self.year

    def __repr__(self):
        return "<Year(%s)>" % self.year

    @property
    def serialize(self):
        return dict('year', self.year)

vehicle_engines = Table('vehicle_engines', db.Base.metadata,
        Column('engine_id', Integer, ForeignKey('engines.id_'),
            primary_key=True),
        Column('year_id', Integer, ForeignKey('years.id_')),
        Column('make_id', Integer, ForeignKey('makes.id_')),
        Column('model_id', Integer, ForeignKey('models.id_')),
        )

class Engine(db.Base):
    __tablename__ = 'engines'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    makes = relationship('Make', secondary=vehicle_engines)
    models = relationship('Model', secondary=vehicle_engines)
    years = relationship('Year', secondary=vehicle_engines)
    parts = relationship('Part', secondary=engine_parts, lazy='dynamic')

    def __unicode__(self):
        return "%s" % self.name

    @property
    def serialize(self):
        return self.name


engine_parts = Table('engine_parts', db.Base.metadata,
        Column('vehicle_guid', GUID(), ForeignKey('vehicles.guid')),
        Column('part_guid', GUID(), ForeignKey('parts.guid')))


class Part(db.Base):
    __tablename__ = 'parts'

    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    desc_short = Column(String)
    desc_long = Column(Text)
    url = Column(String)

    def __unicode__(self):
        return self.name

    @property
    def serialize(self):
        return {'name': self.name,
                'desc_short': self.desc_short,
                'url': self.url}

def get_or_create(session, obclass, **kwargs):
    result = obclass.query.filter_by(**kwargs).first()
    if not result:
        print "Item does not exist, creating"
        result = obclass(**kwargs)
        session.add(result)
    else:
        print "Item exists, returning"
    return result

def import_products(product_filename):
    import codecs
    import csv
    with open(product_filename) as product_file:
        products = csv.DictReader(product_file)
        for product in products:
            new_prod = get_or_create(db.session, Part,
                    name = product['Name'].decode('ascii', 'ignore'),
                    desc_short = product['ShortDescription'].decode('ascii', 'ignore'),
                    desc_long = product['LongDescription'].decode('ascii', 'ignore'),
                    url = product['ProductUrl'].decode('ascii', 'ignore'))
            print new_prod
        db.session.commit()

def import_data(data_filename):
    import codecs
    from csv import reader
    with open(data_filename) as data_file:
        data_reader = reader(data_file, delimiter=",")
        for row in data_reader:
            year, make, model = row
            year = get_or_create(db.session, Year, year = int(year.decode('ascii', 'ignore')))
            make = get_or_create(db.session, Make, name = make.decode('ascii', 'ignore'))
            model = get_or_create(db.session, Model, name = model.decode('ascii', 'ignore'))
            model.make = make
            model.configs.append(Config(year = year))
            db.session.commit()
            print ", ".join([str(year.year), make.name, model.name])
