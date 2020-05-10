#! /usr/bin/env python3

"""Helper functions to assist with development"""

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
