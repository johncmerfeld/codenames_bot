#! /usr/bin/env python3

"""Helper functions to assist with development"""

import json
import ssl

import pandas as pd
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


def get_top_items(all_items: dict, items_to_return: int):
    """Get top items from items dictionary

    Expecting items dictionary to have the following structure:
     {
        'Manganese': {
          'count': 1,
          'product_of_squares': 10000,
          'words_to_connect': 'Iron'
        },
        'Nickel': {
          'count': 1,
          'product_of_squares': 8281,
          'words_to_connect': 'Iron'
        }
    }"""

    data = {}
    for item, stats in all_items.items():
        data[item] = [stats["product_of_squares"]]

    df = pd.DataFrame(data)
    df = pd.melt(df, value_vars=df.columns)
    df = df.nlargest(items_to_return, "value")

    # gives you the items with top product of square scores
    top_items = df["variable"].to_list()

    # we want to return the other stats as well
    top_items_with_stats = []
    for item, stats in all_items.items():
        if item in top_items:
            top_items_with_stats.append({item: stats})

    return top_items_with_stats


def beautify_clues(clues: list):
    """Return clues as string

    Expecting clues list to have the following structure:

    [
        {
            "Mineral": {
                "count": 2,
                "product_of_squares": 32798529,
                "words_to_connect": ["Iron", "Spring"],
            }
        },
        {
            "Sulphur": {
                "count": 2,
                "product_of_squares": 17715681,
                "words_to_connect": ["Iron", "Spring"],
            }
        }
    ]"""

    return json.dumps(clues, indent=4)
