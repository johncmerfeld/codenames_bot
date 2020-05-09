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
        "red": ["Fair", "Fish", "Dinosaur"],
        "blue": ["Drill", "Hollywood"],
        "assassin": ["Foot"],
    }

    my_game = game.Game(
        client, settings.MONGO_DATABASE, settings.collection, words_by_team
    )

    print(my_game.get_words("red"))
    my_game.remove_words("Fair")
    print(my_game.get_words("red"))
    my_game.add_words("Turkey", "red")
    print(my_game.get_words("red"))
    print(my_game.give_clues("red", 5))
