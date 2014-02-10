import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref
from database import Base
from custom_types import GUID

class Make(Base):
    __tablename__ = 'makes'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    models = relationship("Model", backref='make')

    def __unicode__(self):
        return "%s" % self.name
    
    def __repr__(self):
        return "<Make(name='%r')>" % self.name


class Model(Base):
    __tablename__ = 'models'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    make_id = Column(Integer, ForeignKey('makes.id_'))
    years = relationship("Year", secondary=model_year)
    
    def __unicode__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return "<Model(name='%r', make='%r')>" % (
                self.name, self.make.name)


model_year = Table('year_table', Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id_')),
    Column('year_id', Integer, ForeignKey('years.id_'))
)


class Year(Base):
    __tablename__ = 'years'

    id_ = Column(Integer, primary_key=True)
    year = Column(Integer)

    def __unicode__(self):
        return "%d" % self.year

    def __repr__(self):
        return "<Year(%r)>" % self.year


class Engine(Base):
    __tablename__ = 'engines'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    config = Column(String)
    cylinders = Column(Integer)
    size_liter = Column(String)
    size_cid = Column(Integer)

    def __unicode__(self):
        return "%s" % self.name


class Vehicle(Base):
    __tablename__ = 'vehicles'

    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    year_id = Column(Integer, ForeignKey('years.id_'))
    make_id = Column(Integer, ForeignKey('makes.id_'))
    model_id = Column(Integer, ForeignKey('models.id_'))
    engine_id = Column(Integer, ForeignKey('engines.id_'))
    year = relationship("Year")
    make = relationship("Make")
    model = relationship("Model")
    engine = relationship("Engine")

    def __unicode__(self):
        "%d %s %s %s" % (
                self.year.year,
                self.make.name,
                self.model.name,
                self.engine.name
            )

    def __repr__(self):
        return "<Vehicle(guid=%r)>" % (self.guid)


vehicle_parts


class Part(Base):
    __tablename__ = 'parts'

    guid = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    desc_short = Column(String)
    desc_long = Column(Text)
