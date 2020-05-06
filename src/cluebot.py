import settings
import helpers
import itertools

"""Example usage

import cluebot
cluebot.best_connecting_word('blood', 'hood')

cluebot.best_clue(['Drill', 'Lemon', 'Slip', 'Date'])

"""

client = helpers.get_mongo_client(
    settings.MONGO_CLUSTER,
    settings.MONGO_DATABASE,
    settings.MONGO_USER,
    settings.MONGO_PASSWORD,
)

# TODO need to account for rules against parts of words...
def best_connecting_word(base1, base2):
    """Get the word that best connects the pair of base words"""

    print(f"Matching {base1} and {base2}...")

    match_list = []

    for type in ["stimulus", "response"]:
        for pos in ["noun", "verb", "adjective", "adverb"]:
            entry1 = helpers.get_document(
                client,
                settings.MONGO_DATABASE,
                settings.collection,
                text=base1,
                type=type,
                pos=pos,
            )

            entry2 = helpers.get_document(
                client,
                settings.MONGO_DATABASE,
                settings.collection,
                text=base1,
                type=type,
                pos=pos,
            )

            for word1 in entry1["items"]:
                for word2 in entry2["items"]:
                    if word1["item"] == word2["item"]:
                        weight1 = word1["weight"] / 100
                        weight2 = word2["weight"] / 100
                        print(
                            f"{word1['item']} is a match with score of {weight1 * weight2}"
                        )
                        match_list.append(
                            {"word": word1["item"], "score": weight1 * weight2}
                        )

    return best_match(match_list)

def best_match(match_list):
    best_score = 0
    best_match = {}
    for match in match_list:
        if match["score"] > best_score:
            best_match = match
            best_score = match["score"]

    return best_match

# TODO this is doubling the work; only need the upper triangle of the matrix
def best_clue(word_list, k=2):
    """Get the best pairwise connecting word from a group of words"""
    # create empty best_match_list
    best_match_list = []
    # for each pair of words in word_list:
    for pair in itertools.combinations(word_list, k):
        word1 = pair[0]
        word2 = pair[1]
        # get best_match and the overlap score
        connection = best_connecting_word(word1, word2)

        # add the base words, the match word, and the score to best_match_list
        best_match_list.append(
            {
                "word1": word1,
                "word2": word2,
                "connector": connection["word"],
                "score": connection["score"],
            }
        )

    return best_match(best_match_list)
