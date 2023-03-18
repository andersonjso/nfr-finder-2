import csv
import json
#'spring-security', 'spring-boot'
systems = ['spring-security', 'spring-boot', 'spring-framework']

all_locations = {}
n = 0
all_nfrs = []
maint = []
rob = []
perf = []
sec = []
all_keywords = []
for system in systems:
    identification_file_path = f'data/dataset.csv'

    with open(identification_file_path, mode='r', encoding="utf8") as identification_file:
        reader = csv.DictReader(identification_file)
        n = 0
        output = {}
        for row in reader:
            if row['NFR_TYPE']:
                n += 1
                nfrs = row['NFR_TYPE'].replace(" ", "").split(",")


                all_nfrs.extend(nfrs)

                if row['KEYWORDS']:
                    keywords = row['KEYWORDS'].replace("-", "").split(",")
                    all_keywords.extend(keywords)
                    # locations = []
                # if row['LOCATION']:
                #     locations = row['LOCATION'].split(",")
                #
                if "Maintainability" in nfrs:
                    maint.extend(keywords)

                if "Security" in nfrs:
                    sec.extend(keywords)

                if "Robustness" in nfrs:
                    rob.extend(keywords)

                if "Performance" in nfrs:
                    perf.extend(keywords)
                    # #print (nfrs, locations)
                    # for loc in locations:
                    #     loc = loc.replace(" ", "").lower()
                    #     if loc in all_locations:
                    #         all_locations[loc] += 1
                    #     else:
                    #         all_locations[loc] = 1
    print (n)

# my_dict = {i:all_nfrs.count(i) for i in all_nfrs}
# print (my_dict)
my_dict = {i:int(perf.count(i)/3) for i in perf}
sorted_d = {k: v for k, v in sorted(my_dict.items(), key=lambda item: item[1], reverse=True)}
print(json.dumps(sorted_d, indent=2))


# print (*all_keywords, sep='\n')

# print (json.dumps(all_locations, indent=4))