import requests
import json

project = {}

class ListaDeRepositorios():

    def __init__(self, usuario):
        self._usuario = usuario

    def requisicao_api(self):
        page = 1
        params = {'sha': 'main', 'page': page, 'per_page': 100}
        another_page = True
        headers = {'Authorization': 'Bearer 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'}
        api = f'https://api.github.com/repos/spring-projects/spring-framework/commits'
        results = []
        while another_page:  # the list of teams is paginated
            r = requests.get(api, headers=headers, params=params)
            json_response = json.loads(r.text)
            results.extend(json_response)

            if json_response:
                page += 1
                params = {'sha': 'main', 'page': page, 'per_page': 100}
            else:
                another_page = False

        return results

    def imprime_repositorios(self):
        commits = self.requisicao_api()

        with open(f"commit-da-galera.json", "w") as write_file:
            json.dump(commits, write_file, indent=4)



def add_to_author(dict_out, author, commit):
    if author in dict_out:
        dict_out[author]['commits'].append(commit)
    else:
        dict_out[author] = {}
        dict_out[author]['commits'] = []

        dict_out[author]['commits'].append(commit)


repositorios = ListaDeRepositorios('spring-projects')
repositorios.imprime_repositorios()

with open(f"commit-da-galera.json") as commits_file:
    data = json.load(commits_file)
    out = {}
    for commit in data:
        try:
            hash = commit['sha']
            author_login = commit['author']['login']

            add_to_author(out, author_login, hash)
        except:
            print (commit['sha'])

    with open(f"lista_commits_spring_framework.json", "w") as write_file:
        json.dump(out, write_file, indent=4)

