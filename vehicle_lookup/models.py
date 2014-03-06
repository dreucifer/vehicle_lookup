import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
import vehicle_lookup.database as db
from vehicle_lookup.custom_types import GUID

class Level():
    id_ = Column(Integer, primary_key=True)
    name = Column(String)

    def __unicode__(self):
        return "%s" % self.name

    @property
    def serialize(self):
        return {'Name': self.name, 'ID': self.id_}


make_type = Table('make_type', db.Base.metadata,
        Column('make_id', Integer, ForeignKey('makes.id_'), primary_key=True),
        Column('type_id', Integer, ForeignKey('types.id_'), primary_key=True))

class Make(Level, db.Base):
    __tablename__ = 'makes'

    types = relationship('Type', secondary=make_type, lazy='dynamic')


class Type(Level, db.Base):
    __tablename__ = 'types'


modelyear = Table('modelyear', db.Base.metadata,
        Column('model_id', Integer, ForeignKey('models.id_'), primary_key=True),
        Column('year_id', Integer, ForeignKey('years.id_'), primary_key=True))

class ModelYearEngine(Level, db.Base):
    __tablename__ = 'modelyearengine'

    model_id = Column(Integer, ForeignKey('models.id_'))
    year_id = Column(Integer, ForeignKey('years.id_'))
    engine_id = Column(Integer, ForeignKey('engines.id_'))
    engine = relationship('Engine')

class Model(Level, db.Base):
    __tablename__ = 'models'

    type_id = Column(Integer, ForeignKey('types.id_'), nullable=False)
    make_id = Column(Integer, ForeignKey('makes.id_'), nullable=False)
    make = relationship('Make', uselist=False)
    type_ = relationship('Type', uselist=False)
    years = relationship('Year', secondary=modelyear, lazy='dynamic')
    engines = relationship('ModelYearEngine')


class Year(Level, db.Base):
    __tablename__ = 'years'


class Engine(Level, db.Base):
    __tablename__ = 'engines'


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
