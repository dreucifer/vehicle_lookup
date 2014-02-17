#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine, MetaData, Table, distinct
from sqlalchemy.engine import reflection
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///vehicle.db')
metadata = MetaData()
session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine))

Base = declarative_base()
Base.query = session.query_property()

def reflect_temp():
    vehicles_temp = Table("vehicles_temp", metadata)
    inspector = reflection.Inspector.from_engine(engine)
    inspector.reflecttable(vehicles_temp, None)
    return (vehicles_temp, inspector)

def build_data():
    import vehicle_lookup.models
    Base.metadata.create_all(engine)
