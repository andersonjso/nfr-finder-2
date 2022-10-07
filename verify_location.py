import csv
import json
#'spring-security', 'spring-boot'
systems = ['spring-security', 'spring-boot', 'spring-boot']

all_locations = {}
for system in systems:
    identification_file_path = f'data/identification_{system}.csv'

    with open(identification_file_path, mode='r', encoding="utf8") as identification_file:
        reader = csv.DictReader(identification_file)

        output = {}
        for row in reader:
            if row['NFR_TYPE']:
                nfrs = row['NFR_TYPE'].replace(" ", "").replace("-", "None").split(",")
                locations = []
                if row['LOCATION']:
                    locations = row['LOCATION'].split(",")

                if "Maintainability" in nfrs:
                    #print (nfrs, locations)
                    for loc in locations:
                        loc = loc.replace(" ", "").lower()
                        if loc in all_locations:
                            all_locations[loc] += 1
                        else:
                            all_locations[loc] = 1

print (json.dumps(all_locations, indent=4))