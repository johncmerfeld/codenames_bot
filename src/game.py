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

    def validate_team(self, team):
        """Validate team input variable"""

        valid_teams = list(self.words_by_team.keys())
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

    def get_best_connecting_words(self, words):
        """Get best connecting words. This is work in progress!"""

        for word in words:
            helpers.get_document(self.client, self.database, self.collection, text=word)

            # do a bunch of other stuff here
            # remember to avoid other team and assassin
            # the point is that this method should inherent client, database and collection
            # and also know the state of the game

        return []

    def give_clue(self, team):
        """Give clue for team read or blue"""

        if self.validate_team(team):
            words = self.get_words(team)

        return self.get_best_connecting_words(words)


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
