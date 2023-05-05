import requests
import json
import pandas as pd
from datetime import datetime

project = {}

def requisicao_api(url, nfr_type, system):
    page = 1
    params = {'sha': 'main', 'page': page, 'per_page': 100}
    headers = {'Authorization': 'Bearer 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'}

    repo_owner, repo_name, _, pr_number = url.split("/")[-4:]
    pr_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}'
    prs_response = requests.get(pr_url, headers=headers, params=params)
    prs_data = json.loads(prs_response.text)
    sha = prs_data["head"]["sha"]
    created = prs_data["created_at"]
    # dt = datetime.fromisoformat(created)
    # formatted_date = created.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Get the list of files changed in the PR
    files_url = prs_data["url"] + "/files"
    files_response = requests.get(files_url, headers=headers)
    files_data = files_response.json()

    for file in files_data:
        if file['filename'].endswith(".java") and 'test' not in file['filename'].lower():
            # Get the commit history of the file
            commits_before_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file['filename']}&since={created}"
            commits_after_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file['filename']}&sha={sha}"
            # commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file['filename']}"
            # print(commits_url)
            commits_before_response = requests.get(commits_before_url, headers=headers, params=params)
            commits_before_data = commits_before_response.json()

            commits_after_response = requests.get(commits_after_url, headers=headers, params=params)
            commits_after_data = commits_after_response.json()

            # Count the number of commits
            num_commits_before = len(commits_before_data)
            num_commits_after = len(commits_after_data)

            # print (file['filename'].split("/")[-1], num_commits)
            filename = file['filename'].split("/")[-1]
            print(f"{system}, {nfr_type}, {filename}, {num_commits_before}, {num_commits_after}")


if __name__ == '__main__':
    nfrs = ["Maintainability", "Security", "Performance", "Robustness", "None"]

    # Read the CSV file
    system = ["spring-security", "spring-framework", "spring-boot"]
    df = pd.read_csv(f"identification-{system[2]}.csv")

    # Filter the rows by NFR type
    # nfr_type = "Maintainability"

    for nfr_type in nfrs:
        df_nfr = df[df["NFR_TYPE"].fillna("").str.contains(nfr_type)]

        # Extract the URLs
        urls = df_nfr["URL"].tolist()

        # Print the URLs
        print(f"Pull Requests for {nfr_type}:")
        for url in urls:
            try:
                requisicao_api(url, nfr_type, system[2])
            except (AttributeError, ValueError, KeyError) as e:
                print (e, url)


