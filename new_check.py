import requests

# Define the repository, pull request number, and access token
repo_owner = "spring-projects"
repo_name = "spring-boot"
pr_number = "22164"
access_token = "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"
header = {'Authorization': 'Bearer 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'}
# Define the API endpoint to get the pull request information
pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"

# Send a GET request to the API endpoint with the access token
response = requests.get(pr_url, headers=header)
response_json = response.json()

# Get the SHA of the base commit of the pull request
base_commit_sha = response_json["base"]["sha"]

# Get the list of files changed in the pull request
files_url = response_json["url"] + "/files"
files_response = requests.get(files_url, headers={'Authorization': 'Bearer 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'})
files_data = files_response.json()

# Iterate over the files changed in the pull request
for file in files_data:
    # Get the file path and the SHA of the commit before the pull request
    file_path = file["filename"]
    if file_path.endswith(".java") and 'test' not in file_path.lower():
        before_sha = file["sha"]

        # Define the API endpoint to get the number of changes before the pull request
        changes_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{base_commit_sha}"

        # Send a GET request to the API endpoint with the access token
        response = requests.get(changes_url, headers=header)
        response_json = response.json()

        # Get the list of files changed in the commit before the pull request
        files_changed_before = response_json["files"]

        # Initialize the number of changes before and after the pull request to 0
        changes_before = 0
        changes_after = 0

        # Iterate over the files changed in the commit before the pull request
        for file_before in files_changed_before:
            # Check if the file path matches the file path of the current file changed in the pull request
            if file_before["filename"] == file_path:
                # Get the number of changes made to the file before the pull request
                changes_before = file_before["changes"]
                break

        # Get the number of changes made to the file after the pull request
        changes_after = file["changes"]

        # Print the file path and the number of changes before and after the pull request
        print(f"File: {file_path}")
        print(f"Changes before: {changes_before}")
        print(f"Changes after: {changes_after}")
        print()
