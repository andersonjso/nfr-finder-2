import json

part = 0
no_part = 0
with open('spring-security_info_devs.json') as j_file:
    file = json.load(j_file)

    for user in file:
        if file[user]['participates_all_nfrs_never']:
            no_part += 1
        else:
            part += 1

print (part, no_part)