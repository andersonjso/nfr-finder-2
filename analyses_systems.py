import json
import numpy as np

metrics_to_analyze = ['number_of_merged_prs', 'experience_in_days', 'avg_size_of_commits',
                      'mean_time_between_merged_prs',
                      'number_of_pull_requests_opened', 'pulls_opened', 'number_of_commits', 'pulls_closed',
                      'mean_discussion_duration',
                      'mean_time_between_comments', 'mean_words', 'total_words', 'number_of_comments', 'lines_revised',
                      'number_files_revised',
                      'number_modules_revised', 'number_reviews']


def load_files(system):
    pull_file_path = f'data/metrics/{system}_info_devs.json'
    refactorings_file_path = f'data/metrics/refactorings_{system}.json'
    metrics = f'data/metrics/metrics_output.json'

    with open(pull_file_path) as json_input:
        dev_info = json.load(json_input)

    with open(refactorings_file_path) as json_input:
        refactorings_info = json.load(json_input)

    with open(metrics) as json_input:
        metrics = json.load(json_input)

    return dev_info, refactorings_info, metrics


def define_dict_quartiles(refactorings_info, users_metrics):
    dict_metrics = {}

    for user in users_metrics:
        for metric in metrics_to_analyze:
            if metric in user:
                if metric in dict_metrics:
                    dict_metrics[metric].append(user[metric])
                else:
                    dict_metrics[metric] = []
                    dict_metrics[metric].append(user[metric])

    quartiles_metrics = {}
    for metric in dict_metrics:
        quartiles_metrics[metric] = {}

        quartiles_metrics[metric]["1st"] = np.percentile(list(set(dict_metrics[metric])), 25)
        quartiles_metrics[metric]["median"] = np.percentile(list(set(dict_metrics[metric])), 50)
        quartiles_metrics[metric]["3rd"] = np.percentile(list(set(dict_metrics[metric])), 75)

    all_refs = []
    for dev_name in refactorings_info:
        dev = refactorings_info[dev_name]
        all_refs.append(dev['num_refactorings'])

    quartiles_metrics['refactorings'] = {}
    quartiles_metrics['refactorings']["1st"] = np.percentile(list(set(all_refs)), 25)
    quartiles_metrics['refactorings']["median"] = np.percentile(list(set(all_refs)), 50)
    quartiles_metrics['refactorings']["3rd"] = np.percentile(list(set(all_refs)), 75)

    return quartiles_metrics

def get_group_quartile(dict_quartiles, metric_name, value_metric):
    if value_metric >= dict_quartiles[metric_name]['3rd']:
        return "HIGH"
    elif value_metric <= dict_quartiles[metric_name]['1st']:
        return "LOW"
    else:
        return "MEDIUM"

def get_user_quartiles_metrics(users_metrics, metrics, quartiles_metrics, refactorings_info):
    user_quartiles_metrics = {}
    for user in users_metrics:
        username = user['username']
        user_quartiles_metrics[username] = {}
        for metric in metrics:
            if metric in user:
                user_quartiles_metrics[username][metric] = get_group_quartile(dict_quartiles=quartiles_metrics,
                                                                              metric_name=metric,
                                                                              value_metric=user[metric])
            else:
                user_quartiles_metrics[username][metric] = "NONE"

    for user in refactorings_info:
        if user in user_quartiles_metrics:
            user_quartiles_metrics[user]['refactorings'] = get_group_quartile(dict_quartiles=quartiles_metrics,
                                                                              metric_name='refactorings',
                                                                              value_metric=refactorings_info[user][
                                                                                  'num_refactorings'])
        else:
            user_quartiles_metrics[user] = {}
            user_quartiles_metrics[user]['refactorings'] = get_group_quartile(dict_quartiles=quartiles_metrics,
                                                                              metric_name='refactorings',
                                                                              value_metric=refactorings_info[user][
                                                                                  'num_refactorings'])

    return user_quartiles_metrics


def get_groups_by_nfr(nfr, dev_info):
    print (nfr)
    list_participates = []
    list_commited = []
    list_opened = []
    list_reviewed = []
    list_commented = []

    for current_dev in dev_info:
        dev = dev_info[current_dev]

        if current_dev:
            if dev[f'participates_{nfr}_high']:
                list_participates.append(current_dev)
            if dev[f'commited_{nfr}_high']:
                list_commited.append(current_dev)
            if dev[f'opened_discussion_{nfr}_high']:
                list_opened.append(current_dev)
            if dev[f'commented_{nfr}_high']:
                list_commented.append(current_dev)
            if dev[f'reviewed_{nfr}_high']:
                list_reviewed.append(current_dev)

    # print ("Participates:", list_participates)
    print("Commits:", list_commited)
    print("Opens:", list_opened)
    print("Reviews:", list_reviewed)
    print("Comments:", list_commented)


def merge_dev_info(list_dev_info):
    output = {}
    for current_list in list_dev_info:
        for current_dev_info in current_list:
            if current_dev_info != "":
                if current_dev_info in output:
                    for key in output[current_dev_info]:
                        if isinstance(output[current_dev_info][key], bool):
                            if current_list[current_dev_info][key]:
                                output[current_dev_info][key] = current_list[current_dev_info][key]
                        else:
                            output[current_dev_info][key] += current_list[current_dev_info][key]
                else:
                    output[current_dev_info] = current_list[current_dev_info]

    return output



def merge_ref_info(list_refactoring_info):
    output = {}
    for current_list in list_refactoring_info:
        for current_dev_info in current_list:
            if current_dev_info != "":
                if current_dev_info in output:
                    for key in output[current_dev_info]:
                        output[current_dev_info]['num_refactorings'] += current_list[current_dev_info]['num_refactorings']
                else:
                    output[current_dev_info] = current_list[current_dev_info]

    return output

def get_user_by_username(username, list):
    for item in list:
        if item['username'] == username:
            return item

def verify_if_is_in_output_list(output_list, user_data):
    found = False
    for item in output_list:
        if user_data['username'] == item['username']:
            for key in item:
                if isinstance(item[key], bool):
                    if user_data[key]:
                        item[key] = user_data[key]
                elif isinstance(item[key], int):
                    item[key] += user_data[key]

            found = True

    if not found:
        output_list.append(user_data)


def merge_users_metrics(list_metrics_systems):
    output = []
    for current_list in list_metrics_systems:
        for current_dev_info in current_list:
            if current_dev_info['username'] != "":
                current_user = get_user_by_username(current_dev_info['username'], current_list)
                verify_if_is_in_output_list(output, current_user)

    return output

def combine_systems(list_systems):
    list_dev_info = []
    list_refactoring_info = []
    list_metrics_systems = []

    for current_system in list_systems:
        dev_info, refactorings_info, all_metrics = load_files(current_system)
        metrics_current_system = all_metrics[system]
        users_metrics = metrics_current_system['user_metrics']
        list_dev_info.append(dev_info)
        list_refactoring_info.append(refactorings_info)
        list_metrics_systems.append(users_metrics)

    dev_info = merge_dev_info(list_dev_info)
    refactorings_info = merge_ref_info(list_refactoring_info)
    users_metrics = merge_users_metrics(list_metrics_systems)
    quartiles_metrics = define_dict_quartiles(refactorings_info=refactorings_info, users_metrics=users_metrics)
    user_quartiles_metrics = get_user_quartiles_metrics(users_metrics, metrics_to_analyze, quartiles_metrics, refactorings_info)

    get_groups_by_nfr("all_nfrs", dev_info)
    print("***")
    get_groups_by_nfr("security", dev_info)
    print("***")
    get_groups_by_nfr("robustness", dev_info)
    print("***")
    get_groups_by_nfr("maintainability", dev_info)
    print("***")
    get_groups_by_nfr("performance", dev_info)

    json_formatted_str = json.dumps(user_quartiles_metrics, indent=2)

    with open(f"data/metrics/{list_systems}_info_devs.json", "w") as write_file:
        json.dump(dev_info, write_file, indent=4)

    with open(f"data/metrics/groups_users_metrics_{list_systems}.json", "w") as write_file:
        json.dump(user_quartiles_metrics, write_file, indent=4)




if __name__ == "__main__":
    system = 'spring-boot'

    systems = ['spring-framework', 'spring-security', 'spring-boot']

    combine_systems(systems)
"""
    dev_info, refactorings_info, all_metrics = load_files(system)
    metrics_current_system = all_metrics[system]
    users_metrics = metrics_current_system['user_metrics']
    quartiles_metrics = define_dict_quartiles(refactorings_info=refactorings_info, users_metrics=users_metrics)
    user_quartiles_metrics = get_user_quartiles_metrics(users_metrics, metrics_to_analyze, quartiles_metrics, refactorings_info)
    get_groups_by_nfr("all_nfrs", dev_info)
    print("***")
    get_groups_by_nfr("security", dev_info)
    print("***")
    get_groups_by_nfr("robustness", dev_info)
    print("***")
    get_groups_by_nfr("maintainability", dev_info)
    print("***")
    get_groups_by_nfr("performance", dev_info)
"""



    # print (user_quartiles_metrics['rstoyanchev'])
    # print ("-----------------------")
    # print (user_quartiles_metrics['sbrannen'])



