import json
import statistics

from core.PreProcessing import pre_process_on_text
from core.search_by_keywords import get_nfrs_keywords_and_counts, get_nfrs_counts

project_name = "spring-boot"

file_data = f'data/{project_name}_pulls.json'
groups_nfrs = ['all', 'maint', 'sec', 'perf', 'robu']

with open(file_data) as json_file:
    data = json.load(json_file)


def __get_nfrs_list_messages(messages):
    output = {}
    output["n_all"] = 0
    output["n_maint"] = 0
    output["n_sec"] = 0
    output["n_perf"] = 0
    output["n_robu"] = 0
    output["n_words"] = 0

    for message in messages:
        message_cleaned = pre_process_on_text(message['body'])
        nfrs_message = get_nfrs_keywords_and_counts(message_cleaned)

        output["n_all"] += nfrs_message["n_all"]
        output["n_maint"] += nfrs_message["n_maint"]
        output["n_sec"] += nfrs_message["n_sec"]
        output["n_perf"] += nfrs_message["n_perf"]
        output["n_robu"] += nfrs_message["n_robu"]
        output["n_words"] += len(message_cleaned.split())

    return output


def __get_nfrs_list_commits(commits):
    list_commit_messages = []

    for commit in commits:
        current_message = {}
        current_message["body"] = commit["message"]

        list_commit_messages.append(current_message)

    return __get_nfrs_list_messages(list_commit_messages)


def __compute_median_words_commits(list_commits):
    n_words = []
    for commit in list_commits:
        cleaned_commit = pre_process_on_text(commit["message"])
        n_words.append(len(cleaned_commit.split()))

    try:
        median = statistics.median(n_words)
        return median
    except statistics.StatisticsError:
        return None


"""Check whether this pull request is valid
1. If it has only the title, should be discarded"""
def __validate_pr(pull_to_analyze):
    if pull_to_analyze["body"] == "" and \
            not len(pull_to_analyze["comments"]) and \
            not len(pull_to_analyze["review_comments"]):
        return False

    return True

def __divide_comments_by_user_group(comments):
    list_messages_core = []
    list_messages_contributor = []
    list_messages_newcomer = []

    for comment in comments:
        if comment["user_association"] == "MEMBER" or comment["user_association"] == "OWNER":
            list_messages_core.append(comment)
        elif comment["user_association"] == "CONTRIBUTOR" or comment["user_association"] == "COLLABORATOR":
            list_messages_contributor.append(comment)
        elif comment["user_association"] == "NONE" or comment["user_association"] == "FIRST_TIMER" \
                or comment["user_association"] == "FIRST_TIMER_CONTRIBUTOR":
            list_messages_newcomer.append(comment)

    return list_messages_core, list_messages_contributor, list_messages_newcomer

def __get_number_of_keywords_by_user_type(comments, reviews, dict_out):
    list_messages_core, list_messages_contributor, list_messages_newcomer = __divide_comments_by_user_group(comments)
    reviews_core, reviews_contributor, reviews_newcomer = __divide_comments_by_user_group(reviews)

    list_messages_core.extend(reviews_core)
    list_messages_contributor.extend(reviews_contributor)
    list_messages_newcomer.extend(reviews_newcomer)

    nfrs_core = __get_nfrs_list_messages(list_messages_core)
    nfrs_contributor = __get_nfrs_list_messages(list_messages_contributor)
    nfrs_newcomer = __get_nfrs_list_messages(list_messages_contributor)

    for current_nfr in groups_nfrs:
        dict_out[f'core_{current_nfr}'] = nfrs_core[f'n_{current_nfr}']
        dict_out[f'contributor_{current_nfr}'] = nfrs_contributor[f'n_{current_nfr}']
        dict_out[f'newcomer_{current_nfr}'] = nfrs_newcomer[f'n_{current_nfr}']



def get_message_info(data_to_analyze):
    output = []

    for pull in data_to_analyze['pulls']:

        __is_a_valid_pr = __validate_pr(pull)

        if __is_a_valid_pr:
            current = {}
            current['number'] = pull['number']
            title_cleaned = pre_process_on_text(pull['title'])
            title_nfrs = get_nfrs_counts(title_cleaned)

            description_cleaned = pre_process_on_text(pull['body'])
            description_nfrs = get_nfrs_counts(description_cleaned)

            comments_nfrs = __get_nfrs_list_messages(pull['comments'])
            review_comments_nfrs = __get_nfrs_list_messages(pull['review_comments'])
            commits_nfrs = __get_nfrs_list_commits(pull["commits"])

            current["title_n_words"] = len(title_cleaned.split())
            current["description_n_words"] = len(description_cleaned.split())
            current["comments_n_words"] = comments_nfrs["n_words"]
            current["comments_review_n_words"] = review_comments_nfrs["n_words"]
            current["n_commits"] = len(pull["commits"])
            current["median_words_commits"] = __compute_median_words_commits(pull["commits"])
            __get_number_of_keywords_by_user_type(pull['comments'], pull["review_comments"], current)

            for current_nfr in groups_nfrs:
                current[f'title_{current_nfr}'] = title_nfrs[f'n_{current_nfr}']
                current[f'description_{current_nfr}'] = description_nfrs[f'n_{current_nfr}']
                current[f'comments_{current_nfr}'] = comments_nfrs[f'n_{current_nfr}']
                current[f'review_comments_{current_nfr}'] = review_comments_nfrs[f'n_{current_nfr}']
                current[f'commits_{current_nfr}'] = commits_nfrs[f'n_{current_nfr}']

                current[f"general_{current_nfr}"] = current[f'title_{current_nfr}'] + \
                                                    current[f'description_{current_nfr}'] + \
                                                    current[f'comments_{current_nfr}'] + \
                                                    current[f'review_comments_{current_nfr}'] + \
                                                    current[f'commits_{current_nfr}']

            output.append(current)

    return output

def __get_total_nfrs_system(json_file):
    total_robu = total_maint = total_sec = total_perf = 0

    for pull_info in json_file:
        total_robu += pull_info["general_robu"]
        total_maint += pull_info["general_maint"]
        total_sec += pull_info["general_sec"]
        total_perf += pull_info["general_perf"]

    print (f"Robustez: {total_robu}\n"
           f"Manutenabilidade: {total_maint}\n"
           f"Segurança: {total_sec}\n"
           f"Performance: {total_perf}")





if __name__ == "__main__":
    # nfr_info = get_message_info(data)
    #
    # with open(f"output/{project_name}.json", "w") as write_file:
    #     json.dump(nfr_info, write_file, indent=4)

    with open(f"output/{project_name}.json") as read_file:
        j_file = json.load(read_file)
        total_nfrs = __get_total_nfrs_system(j_file)
