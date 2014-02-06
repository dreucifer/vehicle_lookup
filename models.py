#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///vehicle.db')
Base = declarative_base()

year_table = Table('year_table', Base.metadata,
    Column('model_id', Integer, ForeignKey('models.id_')),
    Column('year_id', Integer, ForeignKey('years.id_'))
)

class Make(Base):
    __tablename__ = 'makes'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    models = relationship("Model", backref='make')

    def __repr__(self):
        return "<Make(name='%r')>" % self.name


class Model(Base):
    __tablename__ = 'models'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    make_id = Column(Integer, ForeignKey('makes.id_'))
    years = relationship("Year", secondary=year_table)
    
    def __repr__(self):
        return "<Model(name='%r', make='%r')>" % (self.name, self.make.name)


class Year(Base):
    __tablename__ = 'years'

    id_ = Column(Integer, primary_key=True)
    year = Column(Integer)

    def __repr__(self):
        return "<Year(%r)>" % self.year


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id_ = Column(Integer, primary_key=True)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    engine = Column(String)

    def __repr__(self):
        return "<Vehicle(year='%r', make='%r', model='%r')>" % (
                self.year, self.make, self.model)


def build_data():
    Base.metadata.create_all(engine)

def main():
    build_data()

if __name__ == '__main__':
    main()
