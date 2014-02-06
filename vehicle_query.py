""" jjj """
import json
import urllib
from sqlalchemy.orm import sessionmaker
from models import engine, Make, Model, Year, Vehicle

api_key = open(".freebase_api_key").read()
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

def run_query(query):
    params = {
            'query': json.dumps(query),
            'key': api_key
            }
    url = service_url + '?' + urllib.urlencode(params)
    return json.loads(urllib.urlopen(url).read())

def result(func, query):
    response = func(query)
    return response['result']

def makes():
    query = [{ 
        'id': None,
        'name': None,
        'type': '/automotive/make'
        }]
    return result(run_query, query)

def models(make_name):
    query = [{
        'id': None,
        'name': None,
        'type': '/automotive/model',
        '/automotive/model/make': [{
            'id': None,
            'name': make_name
            }]
        }]
    model_names = [model['name'].replace(make_name+' ', '') for model in result(run_query, query)]
    return model_names

def years(model_name):
    query = [{
        'id': None,
        'name': model_name,
        'type': '/automotive/model',
        '/automotive/model/model_years': []
        }]
    return result(run_query, query)


def main():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Make).all()

    for make in query:
        print make.name
        session.add_all([Model(name=model, make=make) for model in models(make.name)])
        session.commit()


if __name__ == '__main__':
    main()
