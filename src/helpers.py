#! /usr/bin/env python3

"""
This file may not be needed long term but can be used now to assist with development

To demo, open python3 shell and issue the following:

import settings
import helpers
client = helpers.get_mongo_client(settings.MONGO_CLUSTER, settings.MONGO_DATABASE, settings.MONGO_USER, settings.MONGO_PASSWORD)
helpers.get_document(client, settings.MONGO_DATABASE, settings.collection, "slug")

"""

#python3 -m venv test_env source ./test_env/bin/activate
#

import ssl

import pymongo


def get_mongo_client(cluster, database, user, password):
    """Get MongoDB client"""

    return pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/{database}?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE,
    )


def get_document(client, database, collection, text, type="stimulus", pos="noun"):
    """Get document from collection"""

    db = client[database]
    return db[collection].find_one({"text": text, "type": type, "pos": pos})

def get_all_documents(client, database, collection):
    """Get all documents from collection"""

    db = client[database]
    return db[collection].find({})
