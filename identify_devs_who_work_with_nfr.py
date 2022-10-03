import csv
import json
import traceback

import numpy as np

project = 'spring-boot'

identification_file_path = f'data/identification_{project}.csv'
pull_file_path = f'data/{project}_pulls.json'

with open(pull_file_path) as json_input:
    pull_file = json.load(json_input)


def __identify_participation_times(dict_users, user_name, nfrs, task):
    if user_name in dict_users:
        for nfr in nfrs:
            dict_users[user_name][f'{task}_{nfr.lower()}'] += 1

        if 'None' not in nfrs:
            dict_users[user_name][f'{task}_all_nfrs'] += 1
    else:
        dict_users[user_name] = {}

        all_tasks = ['participates', 'opened_discussion', 'commented', 'reviewed', 'commited']

        for _task in all_tasks:
            dict_users[user_name][f'{_task}_security'] = 0
            dict_users[user_name][f'{_task}_maintainability'] = 0
            dict_users[user_name][f'{_task}_robustness'] = 0
            dict_users[user_name][f'{_task}_performance'] = 0
            dict_users[user_name][f'{_task}_none'] = 0
            dict_users[user_name][f'{_task}_all_nfrs'] = 0

        for nfr in nfrs:
            dict_users[user_name][f'{task}_{nfr.lower()}'] += 1

        if 'None' not in nfrs:
            dict_users[user_name][f'{task}_all_nfrs'] += 1


def __identify_tasks_times(dict_users, user_name, nfrs, task):
    try:
        for nfr in nfrs:
            if f'{task}_{nfr.lower()}' in dict_users[user_name]:
                dict_users[user_name][f'{task}_{nfr.lower()}'] += 1
            else:
                dict_users[user_name][f'{task}_{nfr.lower()}'] = 0
                dict_users[user_name][f'{task}_{nfr.lower()}'] += 1

    except Exception as e:
        print(traceback.format_exc())


def __identify_users_on_pull(pull_number, nfrs, dict_output):
    for pull in pull_file['pulls']:
        if pull["number"] == int(pull_number):
            user_opened = [pull['user_login']]
            users_commented = list(map(lambda current_review: current_review["user_login"], pull['comments']))
            users_reviewed = list(map(lambda current_review: current_review["user_login"], pull['review_comments']))
            users_commited = list(map(lambda current_review: current_review["author"], pull['commits']))

            users_participating = set(user_opened + users_commented + users_reviewed + users_commited)


            try:
                for current_user in users_participating:
                    __identify_participation_times(dict_output, current_user, nfrs, 'participates')

                for current_user in user_opened:
                    # __identify_tasks_times(dict_output, current_user, nfrs, "opened_discussion")
                    __identify_participation_times(dict_output, current_user, nfrs, 'opened_discussion')

                for current_user in users_commented:
                    # __identify_tasks_times(dict_output, current_user, nfrs, "commented")
                    __identify_participation_times(dict_output, current_user, nfrs, 'commented')

                for current_user in users_reviewed:
                    # __identify_tasks_times(dict_output, current_user, nfrs, "reviewed")
                    __identify_participation_times(dict_output, current_user, nfrs, 'reviewed')

                for current_user in users_commited:
                    # __identify_tasks_times(dict_output, current_user, nfrs, "commited")
                    __identify_participation_times(dict_output, current_user, nfrs, 'commited')
            except Exception as e:
                print (e)
                break

            return user_opened, users_commented, users_reviewed, users_commited

    return [], [], []


def __get_quartiles_group(list_nfr):
    out = {}
    out["1st"] = np.percentile(list(set(list_nfr)), 25)
    out["median"] = np.percentile(list(set(list_nfr)), 50)
    out["3rd"] = np.percentile(list(set(list_nfr)), 75)

    return out

def __define_quartiles(users, task):
    sec = []
    maint = []
    perf = []
    rob = []
    none = []
    all = []

    for user in users:
        sec.append(users[user][f'{task}_security'])
        maint.append(users[user][f'{task}_maintainability'])
        perf.append(users[user][f'{task}_performance'])
        rob.append(users[user][f'{task}_robustness'])
        none.append(users[user][f'{task}_none'])
        all.append(users[user][f'{task}_all_nfrs'])

    quartiles = {}
    quartiles["security"] = __get_quartiles_group(sec)
    quartiles["maintainability"] = __get_quartiles_group(maint)
    quartiles["performance"] = __get_quartiles_group(perf)
    quartiles["robustness"] = __get_quartiles_group(rob)
    quartiles["none"] = __get_quartiles_group(none)
    quartiles["all_nfrs"] = __get_quartiles_group(all)

    return quartiles

def __define_groups_interaction(users, quartiles, task):
    for user in users:
        for nfr_quartile in quartiles:
            users[user][f"{task}_{nfr_quartile}_high"] = False
            users[user][f"{task}_{nfr_quartile}_low"] = False
            users[user][f"{task}_{nfr_quartile}_medium"] = False
            users[user][f'{task}_{nfr_quartile}_never'] = False

            if users[user][f'{task}_{nfr_quartile}'] == 0:
                users[user][f'{task}_{nfr_quartile}_never'] = True
            elif users[user][f'{task}_{nfr_quartile}'] >= quartiles[nfr_quartile]['3rd']:
                users[user][f"{task}_{nfr_quartile}_high"] = True
            elif users[user][f'{task}_{nfr_quartile}'] <= quartiles[nfr_quartile]['1st']:
                users[user][f"{task}_{nfr_quartile}_low"] = True
            else:
                users[user][f"{task}_{nfr_quartile}_medium"] = True


with open(identification_file_path, mode='r', encoding="utf8") as identification_file:
    reader = csv.DictReader(identification_file)

    output = {}
    for row in reader:
        if row['NFR_TYPE']:
            nfrs = row['NFR_TYPE'].replace(" ", "").replace("-", "None").split(",")
            __identify_users_on_pull(row["NUMBER_ISSUE"], nfrs, output)
            # __identify_users_tasks(row["NUMBER_ISSUE"], nfrs, output)

    tasks = ['commited', 'opened_discussion', 'commented', 'reviewed', 'participates']

    for task in tasks:
        quartiles = __define_quartiles(output, task)
        __define_groups_interaction(output, quartiles, task)

with open(f"output/{project}_info_devs.json", "w") as write_file:
    json.dump(output, write_file, indent=4)



