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
            commits_before_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file['filename']}&until={created}"
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
            print(f"{system},{nfr_type},{filename},{num_commits_before},{num_commits_after}")

def remove_repeated(csv_file):
    import csv

    data = {}

    # Read in the CSV file and group the data by file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row['file']
            if key not in data:
                data[key] = {'system': row['system'], 'nfr': row['nfr'], 'changes_before': 0, 'changes_after': 0,
                             'count': 0}
            data[key]['changes_before'] += int(row['changes_before'])
            data[key]['changes_after'] += int(row['changes_after'])
            data[key]['count'] += 1

    # Calculate the average of the two last columns for repeated files
    for key, value in data.items():
        if value['count'] > 1:
            value['changes_before'] = round(value['changes_before'] / value['count'])
            value['changes_after'] = round(value['changes_after'] / value['count'])
            value['count'] = 1

    # Write the updated data to a new CSV file with no repeated files
    with open('filename_updated.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['system', 'nfr', 'file', 'changes_before', 'changes_after'])
        for key, value in data.items():
            writer.writerow([value['system'], value['nfr'], key, value['changes_before'], value['changes_after']])

def compute_changes():
    nfrs = ["Maintainability", "Security", "Performance", "Robustness", "None"]

    # Read the CSV file
    systems = ["spring-security", "spring-framework", "spring-boot"]
    # for system in systems:
    system = systems[2]
    df = pd.read_csv(f"identification-{system}.csv")

    # Filter the rows by NFR type
    # nfr_type = "Maintainability"

    for nfr_type in nfrs:
        df_nfr = df[df["NFR_TYPE"].fillna("").str.contains(nfr_type)]

        # Extract the URLs
        urls = df_nfr["URL"].tolist()

        # Print the URLs
        # print(f"Pull Requests for {nfr_type}:")
        for url in urls:
            try:
                requisicao_api(url, nfr_type, system)
            except (AttributeError, ValueError, KeyError) as e:
                pass


if __name__ == '__main__':
    compute_changes()
    # remove_repeated('changes.csv')


