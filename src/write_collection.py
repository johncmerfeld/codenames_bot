#! /usr/bin/env python3

"""
Script to write collection to file
Meant to assist with development
Format output with atom-beautify https://atom.io/packages/atom-beautify

Example usage:
$ python3 write_collection.py --collection words_clean_max

Script writes to test.json by default
test.json is ignored by git
You can write to another file with --output
"""

import argparse
import json

import helpers
import settings


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Writes collection to output file")

    parser.add_argument(
        "--collection", dest="collection", required=True, help="Collection to write",
    )

    parser.add_argument(
        "--output",
        dest="output",
        required=False,
        default="test.json",
        help="Output file",
    )

    args = parser.parse_args()

    client = helpers.get_mongo_client(
        settings.MONGO_CLUSTER,
        settings.MONGO_DATABASE,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
    )

    documents_to_write = []
    for document in helpers.get_document_generator(
        client, settings.MONGO_DATABASE, args.collection
    ):
        documents_to_write.append(document)

    with open(args.output, "w") as f:
        json.dump(documents_to_write, f, default=str)
