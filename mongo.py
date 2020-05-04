import os
import logging
import requests
from pymongo import MongoClient

class MongoDB:
    """
    we need to create a single persistent connection to database.

    Everytime a client calls us, we can simply return the connection instead of creating
    it again and again.
    """
    def __init__(self):
        self.db = MongoClient("mongodb://localhost:27017/")

    def get_database(self):
        return self.db

    def get_client(self, db_name):
        return self.db[db_name]



url = "https://api.wordassociations.net/associations/v1.0/json/search?"
api_key = os.getenv('API_KEY')
headers = {'x-rapidapi-key': api_key}

def get_word_associations(url, api_key):
    """Gets response from API"""





    response = requests.get(url=url, params={'apikey': api_key, 'text':'welcome', 'lang':'en'})

    if response.status_code == 200:
        return response.json()['data']['covid19Stats']
    elif response.status_code == 401:
        logging.warning('Invalid or missing API key!')
    else:
        logging.warning('Something went wrong with the request!')

def get_word_list():
    """Return the 400 Codenames words as a list"""
    with open("codenames_words.txt") as f:
        raw = f.readlines()

    word_list = []
    for line in raw:
        word_list.append(line.split("\t"))

    word_list = [item.strip("\n") for sublist in word_list for item in sublist]
    return word_list


# TODO, gotta write some get and insert code...
