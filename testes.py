import json

# Load the JSON data from file
with open('proportion_nfrs.json', 'r') as f:
    data = json.load(f)

# Iterate over the data
for framework, categories in data.items():
    print(f"Framework: {framework}")
    for category, authors in categories.items():
        print(f"  Category: {category}")
        for author in authors:
            try:
                print(f"    Author: {author['author']}")
                print(f"    Participations: {author['participations']}")
                print(f"    Title %: {author['title_%']}")
                print(f"    Description %: {author['description_%']}")
                print(f"    Comment %: {author['comment_%']}")
                print(f"    Revision %: {author['revision_%']}")
                print(f"    Commit %: {author['commit_%']}")
                print(f"    Total %: {author['total_%']}")
            except:
                print ("eae")
