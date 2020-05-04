#! /usr/bin/env python3

"""
Script to write collection to file
Meant to assist with development
Format output with atom-beautify https://atom.io/packages/atom-beautify

Execute with:
$ python3 write_collection_to_file.py
"""

import json

import helpers
import settings


if __name__ == "__main__":

    client = helpers.get_mongo_client(
        settings.MONGO_CLUSTER,
        settings.MONGO_DATABASE,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
    )

    documents_to_write = []
    for document in helpers.get_document_generator(
        client, settings.MONGO_DATABASE, settings.collection
    ):
        del document["_id"]
        documents_to_write.append(document)

    # test.json is in gitignore
    with open("test.json", "w") as f:
        json.dump(documents_to_write, f)
