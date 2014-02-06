#!/bin/env python
""" Vehicle Parts Lookup """

import json

from flask import Flask, redirect, url_for
from sqlalchemy.orm import sessionmaker
from models import engine, Make, Model, Year, Vehicle

app = Flask("vl")
app.debug = True

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return "Hello, world"

@app.route('/vehicle/')
@app.route('/vl/', defaults={'make': None, 'model': None, 'year': None})
@app.route('/vl/<make>/', defaults={'model': None, 'year': None})
@app.route('/vl/<make>/<model>/', defaults={'year': None})
@app.route('/vl/<make>/<model>/<int:year>/')
def vl(*args, **kwargs):
    output = []
    if kwargs['make']:
        output.append('has make')
        if kwargs['model']:
            output.append('has model')
            if kwargs['year']:
                output.append('has year')
            else:
                return "year list"
        else:
            return "model list"
    else:
        return "make list"

if __name__ == '__main__':
    app.run()
