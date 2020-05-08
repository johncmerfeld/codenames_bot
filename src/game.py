#! /usr/bin/env python3

"""
Just run the script:

python3 game.py
"""

import helpers
import settings


class Game:
    def __init__(self, client, database, collection, words_by_team):
        """Class to play the game"""
        self.client = client
        self.database = database
        self.collection = collection
        self.words_by_team = words_by_team

    def get_valid_teams(self):
        """Get the set of valid teams"""

        return list(self.words_by_team.keys())

    def validate_team(self, team):
        """Validate team input variable"""

        valid_teams = self.get_valid_teams()
        valid_teams_string = ", ".join(valid_teams)

        if team not in valid_teams:
            raise Exception(
                f"{team} team not found. Expecting team {valid_teams_string}"
            )
        else:
            return True

    def get_words(self, team):
        """Get words by team"""

        if self.validate_team(team):
            return self.words_by_team[team]

    def add_words(self, word_or_words, team):
        """Add words to team"""

        if self.validate_team(team):
            if isinstance(word_or_words, str):
                if word_or_words not in self.words_by_team[team]:
                    self.words_by_team[team].append(word_or_words)
                    print(f"{word_or_words} added to {team}")
            elif isinstance(word_or_words, (list, tuple)):
                for word in word_or_words:
                    if word not in self.words_by_team[team]:
                        self.words_by_team[team].append(word)
                    print(f"{word} added to {team}")
            else:
                raise Exception(
                    f"Expecting str, list or tuple but got {type(word_or_words).__name__}"
                )

    def remove_words(self, word_or_words):
        """Remove words from game"""

        if isinstance(word_or_words, str):
            for team, team_words in self.words_by_team.items():
                if word_or_words in team_words:
                    team_words.remove(word_or_words)
                    print(f"{word_or_words} removed from {team}")
        elif isinstance(word_or_words, (list, tuple)):
            for team, team_words in self.words_by_team.items():
                for word in word_or_words:
                    if word in team_words:
                        team_words.remove(word)
                        print(f"{word} removed from {team}")

    def get_best_connecting_words(self, words_to_connect, words_to_avoid):
        """Get best connecting words"""

        all_items = {}

        for word in words_to_connect:
            document = helpers.get_document(
                self.client, self.database, self.collection, text=word
            )
            for item, weight in document["weights"].items():
                if item not in words_to_avoid:
                    if item in all_items:
                        all_items[item]["count"] += 1
                        all_items[item]["product_of_squares"] *= weight ** 2
                    else:
                        all_items[item] = {}
                        all_items[item]["count"] = 1
                        all_items[item]["product_of_squares"] = weight ** 2

        return all_items

    def give_clue(self, team):
        """Give clue for team"""

        if self.validate_team(team):
            words_to_connect = self.get_words(team)
            words_to_avoid = []
            for valid_team in self.get_valid_teams():
                if valid_team != team:
                    for word in self.get_words(valid_team):
                        words_to_avoid.append(word)

        return self.get_best_connecting_words(words_to_connect, words_to_avoid)


client = helpers.get_mongo_client(
    settings.MONGO_CLUSTER,
    settings.MONGO_DATABASE,
    settings.MONGO_USER,
    settings.MONGO_PASSWORD,
)

words_by_team = {
    "red": ["Iron", "Lemon", "Fair"],
    "blue": ["Drill", "Hollywood"],
    "assassin": "Foot",
}

game = Game(client, settings.MONGO_DATABASE, settings.collection, words_by_team)

print(game.get_words("red"))
game.remove_words(("Lemon", "Fair"))
print(game.get_words("red"))
game.add_words("Spring", "red")
print(game.get_words("red"))
print(game.give_clue("red"))
