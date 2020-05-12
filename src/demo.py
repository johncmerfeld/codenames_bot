#! /usr/bin/env python3

"""
Demo of game class. Run with:
$ python3 demo.py
"""

import game
import settings
import helpers

if __name__ == "__main__":

    client = helpers.get_mongo_client(
        settings.MONGO_CLUSTER,
        settings.MONGO_DATABASE,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
    )

    words_by_team = {
        "red": [
            "Link",
            "Angel",
            "England",
            "Bugle",
            "Cell",
            "Penguin",
            "Greece",
            "Trip",
            "Hook",
        ],
        "blue": ["Palm", "Tower", "Scuba Diver", "Comic", "Ice Cream", "Water"],
        "nuetral": ["Yard", "Pyramid", "Battery", "Log", "Australia", "Ice", "Disease"],
        "assassin": ["Pistol"],
    }

    g = game.Game(client, settings.MONGO_DATABASE, settings.collection, words_by_team)

    print(g.give_clues("red", 5))
