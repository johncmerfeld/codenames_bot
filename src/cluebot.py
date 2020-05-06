import helpers
import itertools

"""
Example usage

import cluebot
import helpers
import settings

client = helpers.get_mongo_client( \
    settings.MONGO_CLUSTER, \
    settings.MONGO_DATABASE, \
    settings.MONGO_USER, \
    settings.MONGO_PASSWORD, \
)

cluebot.get_best_connecting_word( \
    client, settings.MONGO_DATABASE, settings.collection, "blood", "hood" \
)

cluebot.get_best_clue( \
    client, settings.MONGO_DATABASE, settings.collection, ["Drill", "Lemon", "Slip"] \
)

"""

# TODO need to account for rules against parts of words...


def get_best_connecting_word(client, database, collection, base1, base2):
    """Get the word that best connects the pair of base words"""

    print(f"Matching {base1} and {base2}...")

    entry1 = helpers.get_document(client, database, collection, text=base1)
    entry2 = helpers.get_document(client, database, collection, text=base2)

    match_list = get_match_list(entry1, entry2)

    return get_best_match(match_list)


def get_match_list(entry1, entry2):
    """Get list of matches for pair of entry words"""

    match_list = []
    for word1, weight1 in entry1["weights"].items():
        for word2, weight2 in entry2["weights"].items():
            if word1 == word2:
                score = (weight1 / 100) * (weight2 / 100)
                print(f"{word1} is a match with score of {score}")
                match_list.append({"word": word1, "score": score})

    return match_list


def get_best_match(match_list):
    """Get match with highest score"""

    best_score = 0
    best_match = {}
    for match in match_list:
        if match["score"] > best_score:
            best_match = match
            best_score = match["score"]

    return best_match


# TODO this is doubling the work; only need the upper triangle of the matrix
def get_best_clue(client, database, collection, word_list, k=2):
    """Get the best pairwise connecting word from a group of words"""
    # create empty best_match_list
    best_match_list = []
    # for each pair of words in word_list:
    for pair in itertools.combinations(word_list, k):
        word1 = pair[0]
        word2 = pair[1]
        # get best_match and the overlap score
        connection = get_best_connecting_word(
            client, database, collection, word1, word2
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

    return get_best_match(best_match_list)
