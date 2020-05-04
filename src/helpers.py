#! /usr/bin/env python3

"""
Helper functions to assist with development
"""
import ssl

import pymongo


def get_mongo_client(cluster, database, user, password):
    """Get MongoDB client"""

    return pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{cluster}/{database}?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE,
    )


def get_document(client, database, collection, text, type, pos):
    """Get document from collection"""

    db = client[database]
    return db[collection].find_one({"text": text, "type": type, "pos": pos})


def get_document_generator(client, database, collection):
    """
    Get generator that yields documents in collection
    """

    db = client[database]
    for document in db[collection].find():
        yield document
