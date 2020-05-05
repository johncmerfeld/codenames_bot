import settings
import helpers

client = helpers.get_mongo_client(settings.MONGO_CLUSTER, settings.MONGO_DATABASE, settings.MONGO_USER, settings.MONGO_PASSWORD)

slug = helpers.get_document(client, settings.MONGO_DATABASE, settings.collection, "slug", "response", "noun")
blood = helpers.get_document(client, settings.MONGO_DATABASE, settings.collection, "blood", "response", "noun")


## INCOMPLETE DEMO
print(f"Matching {slug['text']} and {blood['text']}")
for slugword in slug['items']:
    for bloodword in blood['items']:
        if slugword['item'] == bloodword['item']:
            slugweight = slugword['weight'] / 100
            bloodweight = bloodword['weight'] / 100
            print(f"{slugword['item']} is a match with score of {slugweight * bloodweight}")
