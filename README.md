# NFR Finder 2.0

Install the packages by using

<code>pip install -r requirements.txt</code>

<hr>

<code>main.py</code> has an usage example, using the Pull Request file. The file has a list of PRs with all its info.

The output presented on <code>output_sample.json</code> contains the info regarding the keywords.

In that example we are extracting the info from  <strong>title</strong> and <strong>description</strong>. Thus, above we have the number of each NFR with the fields:
- <code>n_all</code>: Number of keywords for <strong>all</strong> NFRs
- <code>n_<NFR_NAME></code>: Number of keywords for the NFR
- <code><NFR_NAME></code>: Keywords for the NFR
- <code>has_nfr</code>: Identify if the message has any type of keyword

<code>ref</code> file contains the refs to the keywords suggested on the comments


![image](https://user-images.githubusercontent.com/2151827/182270709-b14b39bc-c9bd-487b-902e-d2fc1a2e6e45.png)
