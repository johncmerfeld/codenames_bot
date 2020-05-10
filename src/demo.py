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
        "red": ["Port", "Bear", "Platypus", "Africa", "Comic"],
        "blue": ["Knight", "Part", "Ship", "Pumpkin"],
        "nuetral": ["Tower", "Maple", "Space", "Pool", "Flute", "Cotton", "France"],
        "assassin": ["Row"],
    }

    g = game.Game(client, settings.MONGO_DATABASE, settings.collection, words_by_team)

    print(g.give_clues("blue", clues_to_give=5, take_risk=True))
