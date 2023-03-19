import json

from core.search_by_keywords import get_nfrs_keywords_and_counts

investigated_authors_security = ['jgrandja', 'jzheaux', 'rwinch', 'eleftherias', 'marcusdacoregio', 'marcusdacoregio',
                                 'Buzzardo', 'rh-id']

investigated_authors_framework = ['rstoyanchev', 'sbrannen', 'philwebb', 'dreis2211', 'poutsma', 'jhoeller',
                                  'loiclefevre']

investigated_authors_boot = ['izeye', 'dreis2211', 'wilkinsona', 'snicoll', 'Buzzardo', 'philwebb']

def sort_proportion(data_json):
    # Load data from JSON file
    with open(data_json, 'r') as f:
        data = json.load(f)

    for system, nfr_list in data.items():
        for nfr, dev_list in nfr_list.items():
            data[system][nfr] = sorted(dev_list, key=lambda x: float(x['total_%']), reverse=True)

    with open('sorted_devs.json', 'w') as out_file:
        json.dump(data, out_file, indent=4)

def compute_proportions(_investigated_authors, _pull_file, nfr):
    print (f"Computando {nfr}...")
    out_list = []
    for investigated_author in _investigated_authors:
        n_mentioned_title = 0
        total_title = 0
        n_mentioned_body = 0
        total_body = 0
        n_mentioned_comment = 0
        total_comment = 0
        n_mentioned_review = 0
        total_review = 0
        n_mentioned_commit = 0
        total_commit = 0

        total_mentions = 0
        total_participations = 0

        for pull in _pull_file['pulls']:
            participated = False
            mentioned_title = False
            mentioned_body = False
            mentioned_comment = False
            mentioned_review = False
            mentioned_commit = False

            if pull['user_login'] == investigated_author:
                mentioned_title = get_nfrs_keywords_and_counts(pull['title'])
                mentioned_body = get_nfrs_keywords_and_counts(pull['body'])

                if nfr:
                    if mentioned_title[f'n_{nfr}']: n_mentioned_title += 1
                    if mentioned_body[f'n_{nfr}']: n_mentioned_body += 1
                else:
                    if mentioned_title['has_nfr']: n_mentioned_title += 1
                    if mentioned_body['has_nfr']: n_mentioned_body += 1

                total_title += 1
                total_body += 1

                participated = True

            for comment in pull['comments']:
                if comment['user_login'] == investigated_author:
                    mentioned_comment = get_nfrs_keywords_and_counts(comment['body'])

                    if nfr:
                        if mentioned_comment[f'n_{nfr}']: n_mentioned_comment += 1
                    else:
                        if mentioned_comment['has_nfr']: n_mentioned_comment += 1

                    total_comment += 1
                    participated = True

            for review in pull['review_comments']:
                if review['user_login'] == investigated_author:
                    mentioned_review = get_nfrs_keywords_and_counts(review['body'])

                    if nfr:
                        if mentioned_review[f'n_{nfr}']: n_mentioned_review += 1
                    else:
                        if mentioned_review['has_nfr']: n_mentioned_review += 1

                    total_review += 1
                    participated = True

            for commit in pull['commits']:
                if commit['author'] == investigated_author:
                    mentioned_commit = get_nfrs_keywords_and_counts(commit['message'])

                    if nfr:
                        if mentioned_commit[f'n_{nfr}']: n_mentioned_commit += 1
                    else:
                        if mentioned_commit['has_nfr']: n_mentioned_commit += 1

                    total_commit += 1
                    participated = True

            if participated: total_participations += 1

            if mentioned_title or mentioned_body or mentioned_comment or mentioned_review or mentioned_commit:
                total_mentions += 1

        total_mentioned = n_mentioned_title + n_mentioned_body + n_mentioned_comment + n_mentioned_review + n_mentioned_commit
        total_all = total_title + total_body + total_comment + total_review + total_commit

        # print("% of Messages Mentioning NFRs keywords")
        # print(f"Participou em {total_participations} Pulls")
        # if total_title: print("Titulo: {:.2f}%".format((n_mentioned_title / total_title) * 100))
        # if total_body: print("Descrição: {:.2f}%".format((n_mentioned_body / total_body) * 100))
        # if total_comment: print("Comentário: {:.2f}%".format((n_mentioned_comment / total_comment) * 100))
        # if total_review: print("Revisão: {:.2f}%".format((n_mentioned_review / total_review) * 100))
        # if total_commit: print("Commit: {:.2f}%".format((n_mentioned_commit / total_commit) * 100))
        # if total_all: print("Total: {:.2f}%".format((total_mentioned / total_all) * 100))
        if total_participations:
            out = {}
            out['author'] = investigated_author
            out['participations'] = total_participations
            out['title_%'] = "{:.2f}".format((n_mentioned_title / total_title) * 100) if total_title else 0
            out['description_%'] = "{:.2f}".format((n_mentioned_body / total_body) * 100) if total_body else 0
            out['comment_%'] = "{:.2f}".format((n_mentioned_comment / total_comment) * 100) if total_comment else 0
            out['revision_%'] = "{:.2f}".format((n_mentioned_review / total_review) * 100) if total_review else 0
            out['commit_%'] = "{:.2f}".format((n_mentioned_commit / total_commit) * 100) if total_commit else 0
            out['total_%'] = "{:.2f}".format((total_mentioned / total_all) * 100) if total_all else 0

            out_list.append(out)

    return out_list

def save_proportions():
    projects = ['spring-boot', 'spring-framework', 'spring-security']
    nfrs = ['maint', 'sec', 'perf', 'robu']

    output = {}
    for project in projects:
        print(f"Analizando {project}...")
        output[project] = {}

        pull_file_path = f'data/{project}_pulls.json'

        with open(pull_file_path) as json_input:
            pull_file = json.load(json_input)

        with open(f'authors_{project}.json', 'r') as authors_json:
            investigated_authors = json.load(authors_json)

        for nfr in nfrs:
            output[project][nfr] = compute_proportions(investigated_authors, pull_file, nfr)

        print(f"Finalizado {project}!")

    out_file_name = "proportion_nfrs.json"
    with open(out_file_name, 'w') as out_file:
        json.dump(output, out_file, indent=4)

    print(f"Finalizado! Salvo em {out_file_name}.")


def analysis_proportion(data_json):
    with open(data_json, 'r') as f:
        data = json.load(f)

    for system, nfr_list in data.items():
        for nfr, dev_list in nfr_list.items():
            data[system][nfr] = [d for d in dev_list if float(d['total_%']) > 25 and float(d['participations']) > 3]

            print ("eae")

    with open('analyze.json', 'w') as out_file:
        json.dump(data, out_file, indent=4)


if __name__ == "__main__":
    # save_proportions()
    # sort_proportion('proportion_nfrs.json')
    analysis_proportion('sorted_devs.json')




