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
        return self.name


class Make(Level, db.Base):
    __tablename__ = 'makes'



class Type(Level, db.Base):
    __tablename__ = 'types'

    make_id = Column(Integer, ForeignKey('makes.id_'))
    make = relationship('Make', backref='types')


modelyear_engine = Table('modelyear_engine', db.Base.metadata,
        Column('model_id', Integer, ForeignKey('models.id_'), primary_key=True),
        Column('year_id', Integer, ForeignKey('years.id_'), primary_key=True),
        Column('engine_id', Integer, ForeignKey('engines.id_')))

class Model(Level, db.Base):
    __tablename__ = 'models'

    type_id = Column(Integer, ForeignKey('types.id_'), primary_key=True)
    make_id = Column(Integer, ForeignKey('makes.id_'), primary_key=True)
    make = relationship('Make', uselist=False)
    type_ = relationship('Type', uselist=False)
    years = relationship('Year',
            lazy='dynamic',
            secondary=modelyear_engine)
    engines = relationship('Engine',
            lazy='dynamic',
            secondary=modelyear_engine)


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
