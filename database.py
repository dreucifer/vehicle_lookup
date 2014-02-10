#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine, MetaData
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

def build_data():
    import models
    Base.metadata.create_all(engine)
