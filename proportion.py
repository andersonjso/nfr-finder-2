import json

from core.search_by_keywords import get_nfrs_keywords_and_counts

project = 'spring-boot'

pull_file_path = f'data/{project}_pulls.json'

with open(pull_file_path) as json_input:
    pull_file = json.load(json_input)

investigated_authors_security = ['jgrandja', 'jzheaux', 'rwinch', 'eleftherias', 'marcusdacoregio', 'marcusdacoregio',
                        'Buzzardo', 'rh-id']

investigated_authors_framework = ['rstoyanchev', 'sbrannen', 'philwebb', 'dreis2211', 'poutsma', 'jhoeller', 'loiclefevre']

investigated_authors_boot = ['izeye', 'dreis2211', 'wilkinsona', 'snicoll', 'Buzzardo', 'philwebb']

for investigated_author in investigated_authors_boot:
    print (investigated_author)
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

    for pull in pull_file['pulls']:
        participated = False
        mentioned_title = False
        mentioned_body = False
        mentioned_comment = False
        mentioned_review = False
        mentioned_commit = False

        if pull['user_login'] == investigated_author:
            mentioned_title = get_nfrs_keywords_and_counts(pull['title'])
            mentioned_body = get_nfrs_keywords_and_counts(pull['body'])

            if mentioned_title['has_nfr']: n_mentioned_title += 1
            if mentioned_body['has_nfr']: n_mentioned_body += 1

            total_title += 1
            total_body += 1

            participated = True

        for comment in pull['comments']:
            if comment['user_login'] == investigated_author:
                mentioned_comment = get_nfrs_keywords_and_counts(comment['body'])

                if mentioned_comment['has_nfr']: n_mentioned_comment += 1

                total_comment += 1

                participated = True

        for review in pull['review_comments']:
            if review['user_login'] == investigated_author:
                mentioned_review = get_nfrs_keywords_and_counts(review['body'])

                if mentioned_review['has_nfr']: n_mentioned_review += 1

                total_review += 1

                participated = True

        for commit in pull['commits']:
            if commit['author'] == investigated_author:
                mentioned_commit = get_nfrs_keywords_and_counts(commit['message'])

                if mentioned_commit['has_nfr']: n_mentioned_commit += 1

                total_commit += 1

                participated = True

        if participated: total_participations += 1

        if mentioned_title or mentioned_body or mentioned_comment or mentioned_review or mentioned_commit:
            total_mentions += 1

    total_mentioned = n_mentioned_title + n_mentioned_body +  n_mentioned_comment + n_mentioned_review + n_mentioned_commit
    total_all = total_title + total_body + total_comment + total_review + total_commit + total_participations

    print ("% of Messages Mentioning NFRs keywords")
    print (f"Participou em {total_participations} Pulls")
    print ("Titulo: {:.2f}%".format((n_mentioned_title/total_title) * 100))
    print ("Descrição: {:.2f}%".format((n_mentioned_body/total_body) * 100))
    print ("Comentário: {:.2f}%".format((n_mentioned_comment/total_comment) * 100))
    print ("Revisão: {:.2f}%".format((n_mentioned_review/total_review) * 100))
    print ("Commit: {:.2f}%".format((n_mentioned_commit/total_commit) * 100))
    print ("Total: {:.2f}%".format((total_mentioned/total_all) * 100))

