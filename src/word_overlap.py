import settings
import helpers

"""Example usage

import word_overlap
word_overlap.best_connecting_word('blood', 'hood')

"""

client = helpers.get_mongo_client(settings.MONGO_CLUSTER, settings.MONGO_DATABASE, settings.MONGO_USER, settings.MONGO_PASSWORD)

## INCOMPLETE DEMO
def best_connecting_word(base1, base2):
    """Get the word that best connects the pair of base words"""

    print(f"Matching {base1} and {base2}...")

    match_list = []

    for type in ['stimulus', 'response']:
        for pos in ['noun', 'verb', 'adjective', 'adverb']:
            entry1 = helpers.get_document(client,
                                          settings.MONGO_DATABASE,
                                          settings.collection,
                                          base1,
                                          type,
                                          pos)

            entry2 = helpers.get_document(client,
                                          settings.MONGO_DATABASE,
                                          settings.collection,
                                          base2,
                                          type,
                                          pos)

            for word1 in entry1['items']:
                for word2 in entry2['items']:
                    if word1['item'] == word2['item']:
                        weight1 = word1['weight'] / 100
                        weight2 = word2['weight'] / 100
                        print(f"{word1['item']} is a match with score of {weight1 * weight2}")
                        match_list.append({"word": word1['item'], "score": weight1 * weight2})

    best_score = 0
    best_match = {}
    for match in match_list:
        if match['score'] > best_score:
            best_match = match
            best_score = match['score']

    return best_match
