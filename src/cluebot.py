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
# print(cluebot.get_best_clue(['Iron', 'Lemon', 'Fair']))
# print(cluebot.get_best_clue(['Iron', 'Lemon', 'Fair'], algorithm="product_of_weights"))

print(cluebot.get_best_clue(['Iron', 'Slip', 'Tablet', 'Court'], k=2, algorithm="product_of_weights"))
# sometimes cluebot can find a link
print(cluebot.get_best_clue(['Iron', 'Slip', 'Tablet', 'Court'], k=3, algorithm="product_of_weights"))
# sometimes it can't
print(cluebot.get_best_clue(['Iron', 'Lemon', 'Date', 'Court'], k=3, algorithm="product_of_weights"))

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
                helpers.get_document(client, database, collection, text=word)
            )

        match_list = Cluebot.get_match_list(entry_list, algorithm)

        # TODO need to account for rules against parts of words...
        return Cluebot.get_best_match(match_list)

    @staticmethod
    def get_match_list(entry_list, algorithm):
        return Cluebot.get_match_list_recursive(entry_list, algorithm, len(entry_list))

    @staticmethod
    def get_match_list_recursive(entry_list, algorithm, n):
        if n == 2:
            match_list = []
            entry1 = entry_list[0]
            entry2 = entry_list[1]
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
        else:
            match_list = Cluebot.get_match_list_recursive(
                entry_list, algorithm, n - 1
            )
            match_listN = []
            entryN = entry_list[n - 1]
            for wordN, weightN in entryN["weights"].items():
                for match in match_list:
                    if wordN == match['word']:
                        if algorithm == "product_of_squares":
                            score = (weightN ** 2) * (match['score'] ** 2) / 1000000
                        elif algorithm == "product_of_weights":
                            score = (weightN * match['score']) / 100
                        else:
                            score = 0
                        # print(f"{word1} is a match with score of {score}")
                        match_listN.append({"word": wordN, "score": score})
            return match_listN

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
        for word_group in itertools.combinations(word_list, k):
            # get best_match and the overlap score
            connection = Cluebot.get_best_connecting_word(
                self.client, self.database, self.collection, word_group, algorithm
            )


            if not connection:
                print(f"There is no {k}-word match in the group {word_list}")
                return

            # add the base words, the match word, and the score to best_match_list
            else: best_match_list.append(
                {
                    "words": word_group,
                    "connector": connection["word"],
                    "score": connection["score"],
                }
            )

        return Cluebot.get_best_match(best_match_list)
