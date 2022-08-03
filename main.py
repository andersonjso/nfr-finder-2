import json

from PreProcessing import pre_process_on_text
from search_by_keywords import get_nfrs

file_data = 'spring-projects_spring-security_pulls.json'

with open(file_data) as json_file:
    data = json.load(json_file)


def get_message_info(data_to_analyze):
    output = []

    for pull in data_to_analyze['pulls']:
        current = {}
        title_cleaned = pre_process_on_text(pull['title'])
        current["title_nfrs"] = get_nfrs(title_cleaned)

        description_cleaned = pre_process_on_text(pull['body'])
        current["description_nfrs"] = get_nfrs(description_cleaned)

        output.append(current)

    return output


if __name__ == "__main__":
    nfr_info = get_message_info(data)

    with open(f"output.json", "w") as write_file:
        json.dump(nfr_info, write_file, indent=4)

