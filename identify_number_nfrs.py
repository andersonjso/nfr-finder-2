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

def get_authors_working_multiple_projects():
    systems = ['spring-framework', 'spring-security', 'spring-boot']
    output = {}
    for system in systems:
        with open(f'data/metrics/{system}_info_devs.json') as json_input:
            dev_info = json.load(json_input)

            for name in dev_info:
                if name in output:
                    output[name] += 1
                else:
                    output[name] = 1

    sorted_dict = dict(sorted(output.items(), key=lambda item: item[1], reverse=True))

    print(json.dumps(sorted_dict, indent=2))

if __name__ == "__main__":
    get_authors_working_multiple_projects()
    # systems = ['spring-security', 'spring-framework', 'spring-boot']
    #
    # list_out = []
    # for system in systems:
    #     list_out.append(get_number_of_nfrs(system))
    #
    # merged = {key: list_out[0][key] + list_out[1][key] for key in list_out[0]}
    #
    # print("Total")
    # print(json.dumps(merged, indent=4))

