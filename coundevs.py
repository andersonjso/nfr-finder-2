import json

with open('analyze.json', 'r') as inputf:
    data = json.load(inputf)


    for system in data:
        list_devs = []
        print (system)
        print('***')
        for nfr in data[system]:
            list_devs = data[system][nfr]

            print (nfr)
            print ("8888")

            sorted_documents = sorted(list_devs, key=lambda x: float(x["total_%"].split()[0]), reverse=True)

            for doc in sorted_documents[0:10]:
                print(json.dumps(doc, indent=4))