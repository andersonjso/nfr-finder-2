import json
import math
import random

import xlsxwriter

file_data = 'data/spring-projects_spring-security_pulls.json'

SAMPLE_SIZE = 318
PARTICIPANTS = 8
SAMPLE_PARTICIPANT = math.ceil(SAMPLE_SIZE/PARTICIPANTS)
SAMPLE_BY_NFR = math.ceil(SAMPLE_PARTICIPANT/4)

participants = ["Oliveira", "Joao", "Coutinho", "Caio", "Juliana", "Rafael", "Paulo", "Vinicius"]

with open(file_data) as json_file:
    data = json.load(json_file)

def send_to_list(my_dict):
    list_out = []

    for current in my_dict:
        list_out.append(current['number'])

    return list_out

def generate_samples_groups():
    file_data = 'output/output.json'

    with open(file_data) as json_file:
        data = json.load(json_file)

    all = send_to_list(sorted(data, key=lambda d: d['general_all'], reverse=True))
    maint = send_to_list(sorted(data, key=lambda d: d['general_maint'], reverse=True))
    sec = send_to_list(sorted(data, key=lambda d: d['general_sec'], reverse=True))
    perf = send_to_list(sorted(data, key=lambda d: d['general_perf'], reverse=True))
    robu = send_to_list(sorted(data, key=lambda d: d['general_robu'], reverse=True))

    return all, maint, sec, perf, robu


def compute_sample(maint, sec, perf, robu):
    maint_sample = random.sample(maint, SAMPLE_BY_NFR)
    sec = [e for e in sec if e not in set(maint_sample)]
    perf = [e for e in perf if e not in set(maint_sample)]
    robu = [e for e in robu if e not in set(maint_sample)]

    sec_sample = random.sample(sec, SAMPLE_BY_NFR)
    perf = [e for e in perf if e not in set(sec_sample)]
    robu = [e for e in robu if e not in set(sec_sample)]

    perf_sample = random.sample(perf, SAMPLE_BY_NFR)
    robu = [e for e in robu if e not in set(perf_sample)]

    robu_sample = random.sample(robu, SAMPLE_BY_NFR)

    final_sample = []
    final_sample.extend(maint_sample)
    final_sample.extend(sec_sample)
    final_sample.extend(perf_sample)
    final_sample.extend(robu_sample)

    return final_sample


if __name__ == "__main__":
    list_ids = []
    for pull in data['pulls']:
        list_ids.append(pull['number'])

    all, maint, sec, perf, robu = generate_samples_groups()

    workbook = xlsxwriter.Workbook('auxiliar/identification-spring-security.xlsx')
    header = ["NUMBER_ISSUE", "URL", "NFR_TYPE", "PHRASE", "KEYWORDS", "LOCATION", "LABEL"]

    for participant in participants:
        my_sample = compute_sample(maint, sec, perf, robu)

        maint = [e for e in maint if e not in set(my_sample)]
        sec = [e for e in sec if e not in set(my_sample)]
        perf = [e for e in perf if e not in set(my_sample)]
        robu = [e for e in robu if e not in set(my_sample)]

        worksheet = workbook.add_worksheet(participant)

        col = 0
        for header_name in header:
            worksheet.write(0, col, header_name)
            col += 1

        row = 1
        for issue_number in my_sample:
            worksheet.write(row, 0, issue_number)
            worksheet.write(row, 1, f"https://github.com/spring-projects/spring-security/pull/{issue_number}")
            row += 1

    workbook.close()