from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from database import Base
from custom_types import GUID

year_table = Table('year_table', Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id_')),
    Column('year_id', Integer, ForeignKey('years.id_'))
)

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
    years = relationship("Year", secondary=year_table)
    
    def __unicode__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return "<Model(name='%r', make='%r')>" % (self.name, self.make.name)


class Year(Base):
    __tablename__ = 'years'

    id_ = Column(Integer, primary_key=True)
    year = Column(Integer)

    def __unicode__(self):
        return "%d" % self.year

    def __repr__(self):
        return "<Year(%r)>" % self.year


class Vehicle(Base):
    __tablename__ = 'vehicles'

    guid = Column(GUID(), primary_key=True)
    year_id = Column(Integer, ForeignKey('years.id_'))
    make_id = Column(String, ForeignKey('makes.id_'))
    model_id = Column(String, ForeignKey('models.id_'))
    year = relationship("Year")
    make = relationship("Make")
    model = relationship("Model")
    engine = Column(String)

    def __repr__(self):
        return "<Vehicle(year='%r', make='%r', model='%r')>" % (
                self.year, self.make, self.model)
