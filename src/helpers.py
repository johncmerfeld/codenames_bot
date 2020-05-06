#! /usr/bin/env python3

"""
Helper functions to assist with development

Example usage:

import settings
import helpers

client = helpers.get_mongo_client(settings.MONGO_CLUSTER, settings.MONGO_DATABASE, settings.MONGO_USER, settings.MONGO_PASSWORD)
helpers.get_document(client, settings.MONGO_DATABASE, settings.collection_max, text='blood')

"""
import ssl

import pymongo


def get_mongo_client(cluster, database, user, password):
    """Get MongoDB client"""

    return pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/{database}?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE,
    )


def get_document(client, database, collection, **kwargs):
    """Get document from collection"""

    db = client[database]
    return db[collection].find_one(kwargs)


def get_document_generator(client, database, collection):
    """Get generator that yields documents in collection"""

    db = client[database]
    for document in db[collection].find():
        yield document
