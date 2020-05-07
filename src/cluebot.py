import helpers
import itertools

"""
Example usage

import helpers
import settings
from cluebot import Cluebot

client = helpers.get_mongo_client( \
    settings.MONGO_CLUSTER, \
    settings.MONGO_DATABASE, \
    settings.MONGO_USER, \
    settings.MONGO_PASSWORD, \
)

cluebot = Cluebot(client, settings.MONGO_DATABASE, settings.collection)

# will be phased out as outward-facing function
print(cluebot.get_best_clue(['Iron', 'Lemon', 'Fair']))
print(cluebot.get_best_clue(['Iron', 'Lemon', 'Fair'], algorithm="product_of_weights"))

"""

class Cluebot:

    def __init__(self, client, database, collection):
        self.client = client
        self.database = database
        self.collection = collection

    def set_collection(self, new_collection):
        self.collection = new_collection

    @staticmethod
    def get_best_connecting_word(client,
                                 database,
                                 collection,
                                 word_list,
                                 algorithm):
        """Get the word that best connects the pair of base words"""

        # print(f"Matching {base1} and {base2}...")

        entry_list = []
        for word in word_list:
            entry_list.append(
                helpers.get_document(client, database, collection, text=base1)
            )

        match_list = Cluebot.get_match_list(entry_list, algorithm)

        # TODO need to account for rules against parts of words...
        return Cluebot.get_best_match(match_list)

    @staticmethod
    def get_match_list(entry_list, algorithm):
        """Get list of matches for pair of entry words"""

        # TODO: Might need recursion for this!

        match_list = []
        for word1, weight1 in entry1["weights"].items():
            for word2, weight2 in entry2["weights"].items():
                if word1 == word2:
                    if algorithm == "product_of_squares":
                        score = (weight1 ** 2) * (weight2 ** 2) / 1000000
                    elif algorithm == "product_of_weights":
                        score = (weight1 * weight2) / 100
                    else:
                        score = 0
                    # print(f"{word1} is a match with score of {score}")
                    match_list.append({"word": word1, "score": score})

        return match_list

    @staticmethod
    def get_best_match(match_list):
        """Get match with highest score"""

        best_score = 0
        best_match = {}
        for match in match_list:
            if match["score"] > best_score:
                best_match = match
                best_score = match["score"]

        return best_match


    def get_best_clue(self, word_list, k=2, algorithm="product_of_squares"):
        """Get the best pairwise connecting word from a group of words"""
        # create empty best_match_list
        best_match_list = []
        # for each pair of words in word_list:
        for pair in itertools.combinations(word_list, k):
            word1 = pair[0]
            word2 = pair[1]
            # get best_match and the overlap score
            connection = Cluebot.get_best_connecting_word(
                self.client, self.database, self.collection, word1, word2, algorithm
            )

            # add the base words, the match word, and the score to best_match_list
            best_match_list.append(
                {
                    "word1": word1,
                    "word2": word2,
                    "connector": connection["word"],
                    "score": connection["score"],
                }
            )

        return Cluebot.get_best_match(best_match_list)
