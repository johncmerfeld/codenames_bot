#! /usr/bin/env python3

"""
Just run the script:

python3 game.py
"""

import helpers
import settings


class Game:
    def __init__(self, client, database, collection, words):
        """Class to play the game"""
        self.client = client
        self.database = database
        self.collection = collection
        self.words = words

    def get_words(self, key):
        """Get words by key"""

        if key not in ("red", "blue", "assassin"):
            raise Exception(f"{key} not found. Expecting red, blue or assassin")
        else:
            return self.words[key]

    def add_words(self, word_or_words, team):
        """Add words to game"""

        if not isinstance(word_or_words, list):
            raise Exception(f"Expecting list but got {type(word_or_words).__name__}")
        elif team not in ("red", "blue"):
            raise Exception(f"{team} team not found. Expecting team red or blue")
        else:
            for word in word_or_words:
                if word not in self.words[team]:
                    self.words[team].append(word)
                    print(f"{word} added to {team}")

    def remove_words(self, word_or_words):
        """Remove words from game"""

        if not isinstance(word_or_words, list):
            raise Exception(f"Expecting list but got {type(word_or_words).__name__}")
        else:
            for word in word_or_words:
                for key, value in self.words.items():
                    if word in value:
                        value.remove(word)
                        print(f"{word} removed from {key}")

    def get_best_connecting_words(self, words):
        """Get best connecting words. This is work in progress!"""

        for word in words:
            helpers.get_document(self.client, self.database, self.collection, text=word)

            # the point is that this method should inherent client, database and collection
            # and also know the state of the game
            # do a bunch of other stuff here
            # remember to avoid other team and assassin

        return []

    def give_clue(self, team):
        """Give clue for team read or blue"""

        if team not in ("red", "blue"):
            raise Exception(f"{team} team not found. Expecting team red or blue")
        else:
            words = self.get_words(team)

        return self.get_best_connecting_words(words)


client = helpers.get_mongo_client(
    settings.MONGO_CLUSTER,
    settings.MONGO_DATABASE,
    settings.MONGO_USER,
    settings.MONGO_PASSWORD,
)

words = {
    "red": ["Iron", "Lemon", "Fair"],
    "blue": ["Drill", "Hollywood"],
    "assassin": "Foot",
}

game = Game(client, settings.MONGO_DATABASE, settings.collection, words)

print(game.get_words("red"))
game.remove_words(["Iron"])
print(game.get_words("red"))
game.add_words(["Spring"], "red")
print(game.get_words("red"))
print(game.give_clue("red"))
