#! /usr/bin/env python3

"""Demo of game class"""

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
            "Server",
            "Ninja",
            "Tap",
            "Mole",
            "Torch",
            "King",
            "Water",
            "War",
            "Fan",
        ],
        "blue": ["Bottle", "Car", "Wake", "England", "Grass", "Box", "Staff", "Cap"],
        "assassin": ["Yard"],
    }

    my_game = game.Game(
        client, settings.MONGO_DATABASE, settings.collection, words_by_team
    )

    print(my_game.give_clues("blue", clues_to_give=3, metric="sum"))
