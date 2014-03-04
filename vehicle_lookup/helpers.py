import csv
import codecs
import functools
import vehicle_lookup.database as db
from vehicle_lookup.models import Year, Make, Model, Type, Engine, Part

def get_or_create(session, obclass, **kwargs):
    result = obclass.query.filter_by(**kwargs).first()
    if not result:
        print "Item does not exist, creating"
        result = obclass(**kwargs)
    else:
        print "Item exists, returning"
    return result

def import_products(product_filename):
    with open(product_filename) as product_file:
        products = csv.DictReader(product_file)
        for product in products:
            new_prod = get_or_create(db.session, Part,
                    name = product['Name'].decode('ascii', 'ignore'),
                    desc_short = product['ShortDescription'].decode(
                        'ascii', 'ignore'),
                    desc_long = product['LongDescription'].decode(
                        'ascii', 'ignore'),
                    url = product['ProductUrl'].decode('ascii', 'ignore'))
            print new_prod
        db.session.commit()

def import_data(data_filename):
    with open(data_filename) as data_file:
        data_reader = csv.reader(data_file, delimiter=",")
        for row in data_reader:
            year, make, model = row
            year = get_or_create(db.session,
                    Year, year = int(year.decode('ascii', 'ignore')))
            make = get_or_create(db.session,
                    Make, name = make.decode('ascii', 'ignore'))
            model = get_or_create(db.session, Model,
                    name = model.decode('ascii', 'ignore'))
            model.make = make
            db.session.commit()
            print ", ".join([str(year.year), make.name, model.name])

def importer(filename='import.csv'):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with open(filename) as open_file:
                results = []
                file_reader = csv.DictReader(open_file)
                for row in file_reader:
                    ret = func(row)
                    results.append(ret)
                    db.session.commit()
            return results
        return inner
    return decorator

@importer(filename='makes.csv')
def import_makes(row):
    print "Imported {0}".format(row['Name'])
    return get_or_create(db.session,
            Make, name = row['Name'])

@importer(filename='types.csv')
def import_types(row):
    print "imported {0} {1}".format(row['makeName'], row['Name'])
    make = get_or_create(db.session,
            Make, name = row['makeName'])
    return get_or_create(db.session,
            Type, name = row['Name'], make=make)

@importer(filename='models.csv')
def import_models(row):
    with db.session.no_autoflush:
        make = get_or_create(db.session,
                Make, name = row['makeName'])
        vtype = get_or_create(db.session,
                Type, name = row['typeName'])
        model = get_or_create(db.session,
                Model, name = row['Name'],
                make = make,
                type_ = vtype)
    db.session.add(model)
    return model
