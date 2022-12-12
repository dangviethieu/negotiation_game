import csv
import requests  # pip3 install requests
from pprint import pprint

CSV_PATH = 'ID-Part-1.csv'
EN_LANGUAGE = 3
SERVER_URL = 'http://localhost:8000'
REST_KEY = '9340409623470'  # fill this later




class User:
    def __init__(self, id, language, address):
        self.id = id
        self.language = language
        self.address = address

    def __str__(self) -> str:
        return f'User: {self.id}, {self.language}, {self.address}'

def get_user_from_db(id):
    """
    Get user from csv file
    """
    user = None
    try:
        with open(CSV_PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[8] == id:
                    user = User(id, row[6][0], row[5])
    except Exception as e:
        print(e)
    finally:
        return user

def call_api(method, *path_parts, **params) -> dict:
    path_parts = '/'.join(path_parts)
    url = f'{SERVER_URL}/api/{path_parts}/'
    resp = method(url, json=params, headers={'otree-rest-key': REST_KEY})
    if not resp.ok:
        msg = (
            f'Request to "{url}" failed '
            f'with status code {resp.status_code}: {resp.text}'
        )
        raise Exception(msg)
    return resp.json()
