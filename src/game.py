#! /usr/bin/env python3

"""
Class to play the game
Check it out by running demo.py script
"""

import json

import pandas as pd

import helpers


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

    def get_clues(
        self, words_to_connect, words_to_avoid, clues_to_give, metric, clue_type,
    ):
        """
        Get clues

        words_to_connect: words to connect
        words_to_avoid: words to avoid
        clues_to_give: number of clues to give
        metric: metric for which to optimize
        clue_type: stimulus or response

        Returns clues as dictionary
        """

        valid_metrics = ("count", "sum", "product", "product_of_squares")
        valid_metrics_string = ", ".join(valid_metrics)

        data = {}

        for word in words_to_connect:
            document = helpers.get_document(
                self.client, self.database, self.collection, text=word, type=clue_type,
            )
            if document:
                for item_dct in document["items"]:
                    item = item_dct["item"]
                    weight = item_dct["weight"]
                    # we don't want Drilling returned as a word associated with Drill
                    if (
                        item.lower() not in word.lower()
                        and word.lower() not in item.lower()
                    ):
                        if item in data:
                            data[item]["count"] += 1
                            data[item]["sum"] += weight
                            data[item]["product"] *= weight
                            data[item]["product_of_squares"] *= weight ** 2
                            data[item]["words_to_connect_matches"].append(
                                f"{word}: {weight}"
                            )
                        else:
                            data[item] = {}
                            data[item]["count"] = 1
                            data[item]["sum"] = weight
                            data[item]["product"] = weight
                            data[item]["product_of_squares"] = weight ** 2
                            data[item]["words_to_connect_matches"] = [
                                f"{word}: {weight}"
                            ]
                            data[item]["words_to_avoid_matches"] = []
            else:
                print(f"{word} not found in {self.collection}")

        for word in words_to_avoid:
            document = helpers.get_document(
                self.client, self.database, self.collection, text=word
            )
            if document:
                for item_dct in document["items"]:
                    item = item_dct["item"]
                    weight = item_dct["weight"]
                    if item in data:
                        data[item]["words_to_avoid_matches"].append(f"{word}: {weight}")
            else:
                print(f"{word} not found in {self.collection}")

            df = pd.DataFrame(data)
            df = df.transpose()

            try:
                # metrics are stored as dtype objects so we need to convert them
                df[metric] = df[metric].astype("int")
                df = df.nlargest(clues_to_give, metric)

                return df.to_dict("index")

            except KeyError:
                raise Exception(
                    f"{metric} is not a valid metric. Expecting {valid_metrics_string}"
                )

    def give_clues(
        self, team, clues_to_give=3, metric="product_of_squares", clue_type="stimulus",
    ):
        """
        Give clues

        team: team for which to give clues
        clues_to_give: number of clues to give
        metric: metric for which to optimize
        clue_type: stimulus or response

        Returns clues as formatted dictionary
        """

        if self.validate_team(team):
            words_to_connect = self.get_words(team)
            words_to_avoid = []
            for valid_team in self.get_valid_teams():
                if valid_team != team:
                    for word in self.get_words(valid_team):
                        words_to_avoid.append(word)

        clues = self.get_clues(
            words_to_connect, words_to_avoid, clues_to_give, metric, clue_type,
        )

        return json.dumps(clues, indent=4)
