import json

from core.PreProcessing import pre_process_on_text
from core.search_by_keywords import get_nfrs_keywords_and_counts, get_nfrs_counts

file_data = 'data/spring-projects_spring-security_pulls.json'

with open(file_data) as json_file:
    data = json.load(json_file)


def get_nfrs_comments(comments):
    output = {}
    output["n_all"] = 0
    output["n_maint"] = 0
    output["n_sec"] = 0
    output["n_perf"] = 0
    output["n_robu"] = 0

    for comment in comments:
        comment_cleaned = pre_process_on_text(comment['body'])
        nfrs_comment = get_nfrs_keywords_and_counts(comment_cleaned)

        output["n_all"] += nfrs_comment["n_all"]
        output["n_maint"] += nfrs_comment["n_maint"]
        output["n_sec"] += nfrs_comment["n_sec"]
        output["n_perf"] += nfrs_comment["n_perf"]
        output["n_robu"] += nfrs_comment["n_robu"]

    return output



def get_message_info(data_to_analyze):
    output = []

    for pull in data_to_analyze['pulls']:
        current = {}
        current['number'] = pull['number']
        title_cleaned = pre_process_on_text(pull['title'])
        title_nfrs = get_nfrs_counts(title_cleaned)

        current["title_all"] = title_nfrs['n_all']
        current["title_maint"] = title_nfrs['n_maint']
        current["title_sec"] = title_nfrs['n_sec']
        current["title_perf"] = title_nfrs['n_perf']
        current["title_robu"] = title_nfrs['n_robu']

        description_cleaned = pre_process_on_text(pull['body'])
        description_nfrs = get_nfrs_counts(description_cleaned)

        current["description_all"] = description_nfrs['n_all']
        current["description_maint"] = description_nfrs['n_maint']
        current["description_sec"] = description_nfrs['n_sec']
        current["description_perf"] = description_nfrs['n_perf']
        current["description_robu"] = description_nfrs['n_robu']

        comments_nfrs = get_nfrs_comments(pull['comments'])
        current["comments_all"] = comments_nfrs['n_all']
        current["comments_maint"] = comments_nfrs['n_maint']
        current["comments_sec"] = comments_nfrs['n_sec']
        current["comments_perf"] = comments_nfrs['n_perf']
        current["comments_robu"] = comments_nfrs['n_robu']

        review_comments_nfrs = get_nfrs_comments(pull['review_comments'])
        current["review_comments_all"] = review_comments_nfrs['n_all']
        current["review_comments_maint"] = review_comments_nfrs['n_maint']
        current["review_comments_sec"] = review_comments_nfrs['n_sec']
        current["review_comments_perf"] = review_comments_nfrs['n_perf']
        current["review_comments_robu"] = review_comments_nfrs['n_robu']

        current["general_all"] = current["title_all"] + current["description_all"] + current["comments_all"] + current["review_comments_all"]
        current["general_maint"] = current["title_maint"] + current["description_maint"] + current["comments_maint"] + current["review_comments_maint"]
        current["general_sec"] = current["title_sec"] + current["description_sec"] + current["comments_sec"] + current["review_comments_sec"]
        current["general_perf"] = current["title_perf"] + current["description_perf"] + current["comments_perf"] + current["review_comments_perf"]
        current["general_robu"] = current["title_robu"] + current["description_robu"] + current["comments_robu"] + current["review_comments_robu"]

        output.append(current)

    return output


if __name__ == "__main__":
    nfr_info = get_message_info(data)

    with open(f"output.json", "w") as write_file:
        json.dump(nfr_info, write_file, indent=4)

