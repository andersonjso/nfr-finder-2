# NFR Finder 2.0

Install the packages by using <code>pip install -r requirements.txt</code>

<code>ref</code> file contains the refs to the keywords suggested on the comments

<hr>

<code>main.py</code> has an usage example, using the Pull Request file. The file has a list of PRs with all its info.

<code>output_<project_name>.json</code> contains the features

<hr/>

In that output we are extracting the following features:

- <code>number</code>: PR number
<hr/>

- <code>title_n_words</code>: PR title number of words
- <code>description_n_words</code>: PR description number of words
- <code>comments_n_words</code>: PR comments number of words
- <code>comments_review_n_words</code> PR review comments number of words

<hr/>

- <code>n_commits</code> Number of commits associated with the PR
- <code>median_words_commits</code>: Median of words in commits associated with the PR

<hr/>

- <code>core_all</code>: Number of keywords (in general) mentioned by core developers on comments and review comments
- <code>contributor_all</code>: Number of keywords (in general) mentioned by contributors developers on comments and review comments 
- <code>newcomer_all</code>: Number of keywords (in general) mentioned by newcomers developers on comments and review comments
- <code>core_maint</code>: Number of maintainability keywords mentioned by core developers on comments and review comments
- <code>contributor_maint</code>: Number of maintainability keywords mentioned by contributor developers on comments and review comments
- <code>newcomer_maint</code>: Number of maintainability keywords mentioned by newcomer developers on comments and review comments
- <code>core_sec</code>: Number of security keywords mentioned by core developers on comments and review comments
- <code>contributor_sec</code>: Number of security keywords mentioned by contributor developers on comments and review comments
- <code>newcomer_sec</code>: Number of security keywords mentioned by newcomers developers on comments and review comments
- <code>core_perf</code>: Number of performance keywords mentioned by core developers on comments and review comments
- <code>contributor_perf</code>: Number of performance keywords mentioned by contributor developers on comments and review comments
- <code>newcomer_perf</code>: Number of performance keywords mentioned by newcomer developers on comments and review comments
- <code>core_robu</code>: Number of robustness keywords mentioned by core developers on comments and review comments
- <code>contributor_robu</code>: Number of robustness keywords mentioned by contributor developers on comments and review comments
- <code>newcomer_robu</code>: Number of robustness keywords mentioned by newcomer developers on comments and review comments

<hr/>

- <code>title_all</code>: Number of keywords (in general) in PR title
- <code>description_all</code>: Number of keywords (in general) in PR description
- <code>comments_all</code>: Number of keywords (in general) in PR comments
- <code>review_comments_all</code>: Number of keywords (in general) in PR review comments
- <code>commits_all</code>: Number of keywords (in general) in PR associated commits
- <code>general_all</code>: Number of keywords (in general) in all artifacts
- <code>title_maint</code>: Number of maintainability keywords in PR title
- <code>description_maint</code>: Number of maintainability keywords in PR description
- <code>comments_maint</code>: Number of maintainability keywords in PR comments
- <code>review_comments_maint</code>: Number of maintainability keywords in PR review comments
- <code>commits_maint</code>: Number of maintainability keywords in PR associated commits
- <code>general_maint</code>: Number of maintainability keywords in all artifacts
- <code>title_sec</code>: Number of security keywords in PR title
- <code>description_sec</code>: Number of security keywords in PR description
- <code>comments_sec</code>: Number of security keywords in PR comments
- <code>review_comments_sec</code>: Number of security keywords in PR review comments
- <code>commits_sec</code>: Number of security keywords in PR associated commits
- <code>general_sec</code>: Number of security keywords in all artifacts
- <code>title_perf</code>: Number of performance keywords in PR title
- <code>description_perf</code>: Number of performance keywords in PR description
- <code>comments_perf</code>: Number of performance keywords in PR comments
- <code>review_comments_perf</code>: Number of performance keywords in PR review comments
- <code>commits_perf</code>: Number of performance keywords in PR associated commits
- <code>general_perf</code>: Number of performance keywords in all artifacts
- <code>title_robu</code>: Number of robustness keywords in PR title
- <code>description_robu</code>: Number of robustness keywords in PR description
- <code>comments_robu</code>: Number of robustness keywords in PR robustness comments
- <code>review_comments_robu</code>: Number of robustness keywords in PR review comments
- <code>commits_robu</code>: Number of robustness keywords in PR associated commits
- <code>general_robu</code>: Number of robustness keywords in all artifacts