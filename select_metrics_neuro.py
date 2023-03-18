import json
project = 'spring-security'
path = f'data\\metrics\\{project}_info_devs.json'

devs_interest = ['jgrandja', 'Buzzardo', 'rwinch', 'dreis2211', 'jzheaux', 'eleftherias', 'philwebb', 'izeye',
                 'wilkinsona', 'rstoyanchev']

with open(path) as commits_file:
    data = json.load(commits_file)
    output = {}

    for current_dev in devs_interest:
        if current_dev in data:
            output[current_dev] = data[current_dev]

    with open(f"output/{project}_neuro_metrics.json", "w") as write_file:
        json.dump(output, write_file, indent=4)
