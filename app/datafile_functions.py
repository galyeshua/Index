from app import db
from flask import json
from app.models import Data
from time import time


def get_data(filename: str):
    '''
    return dict of data from file or empty formatted dict in case of error in file
    '''
    try:
        with open(filename, 'r') as f:
            categories = json.load(f)
    except FileNotFoundError:
        print(filename + ' does not exists. Creating file.')
        categories = {'categories': []}
        save_data(filename, [])
        print(filename + ' created successfully.')
    except:
        categories = {'categories': [], 'timestamp': 0}

    return categories


def save_data(filename: str, form_data: list):
    '''
    get filename and list of categories
    saves data to a file and db
    '''
    dict_data = {'categories': form_data, 'timestamp': time()}
    with open(filename, 'w') as f:
        json.dump(dict_data, f)
    d = Data(data=json.dumps(dict_data))
    db.session.add(d)
