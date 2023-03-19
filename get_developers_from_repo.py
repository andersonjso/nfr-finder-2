import json

import requests

project = 'spring-security'
def requisicao_api():
    page = 1
    params = {'sha': 'main', 'page': page, 'per_page': 100}
    another_page = True
    headers = {'Authorization': 'Bearer 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'}
    api = f'https://api.github.com/repos/spring-projects/{project}/contributors'
    results = []
    while another_page:  # the list of teams is paginated
        r = requests.get(api, headers=headers, params=params)
        json_response = json.loads(r.text)
        list_authors = [author['login'] for author in json_response]
        results.extend(list_authors)

        if json_response:
            page += 1
            params = {'sha': 'main', 'page': page, 'per_page': 100}
        else:
            another_page = False

    return list(set(results))


def imprime_repositorios():
    authors = requisicao_api()

    with open(f"authors_{project}.json", "w") as write_file:
        json.dump(authors, write_file, indent=4)

if __name__ == '__main__':
    imprime_repositorios()