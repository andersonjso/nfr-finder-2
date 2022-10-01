import csv
import json
from collections import defaultdict

def get_number_of_nfrs(project):
    print (project)
    identification_file_path = f'data/identification_{project}.csv'

    with open(identification_file_path, mode='r', encoding="utf8") as identification_file:
        reader = csv.DictReader(identification_file)

        output = {}
        for row in reader:
            if row['NFR_TYPE']:
                nfrs = row['NFR_TYPE'].replace(" ", "").replace("-", "None").split(",")

                for nfr in nfrs:
                    if nfr in output:
                        output[nfr] += 1
                    else:
                        output[nfr] = 1

        print(json.dumps(output, indent=4))

    return output


if __name__ == "__main__":
    systems = ['spring-security', 'spring-framework']

    list_out = []
    for system in systems:
        list_out.append(get_number_of_nfrs(system))

    merged = {key: list_out[0][key] + list_out[1][key] for key in list_out[0]}

    print("Total")
    print(json.dumps(merged, indent=4))

