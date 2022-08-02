maint_keywords = ["maintainability", "maintenance", "reliability", "serviceability", "accordance", "measures",
                  "requirements", "index", "update", "release", "production", "addition", "budget",
                  "integration", "operation", "comprehension", "readable", "readability"]

perf_keywords = ["performance", "rate", "bandwidth", "cpu", "time", "latency", "throughput", "channel",
                 "instruction", "response", "process", "communication", "space", "memory", "storage", "peak",
                 "compress",
                 "uncompress", "runtime", "perform", "execute", "dynamic", "offset", "reduce", "response", "longer",
                 "fast", "slow", "maximum", "capacity"]

robu_keywords = ["robust", "robustness", "inputs", "error", "failure", "network", "error", "reliability",
                 "serviceability", "fault", "tolerance", "exception", "bug", "recover", "handl", "fail with",
                 "crash", "unexpect", "NPE", "null", "stack", "swallow"]

security_keywords = ["access", "author", "ensure", "data", "authentication", "security", "secure", "malicious",
                     "prevent", "incorrect", "harmful", "state", "exception", "vulnerability", "vulnerable",
                     "malicious", "harmful", 'attack', 'expose', 'compromised', 'aunthenticator', 'encrypt']

all_keywords = []
all_keywords.extend(maint_keywords)
all_keywords.extend(perf_keywords)
all_keywords.extend(robu_keywords)
all_keywords.extend(security_keywords)

all_keywords = list(set(all_keywords))


def _find_in_list(list_nfrs, message):
    list_nfrs_words = []
    count = 0
    for key in list_nfrs:
        if key in message:
            list_nfrs_words.append(key)
            count += 1

    return list_nfrs_words, count


def _has_nfr_in_list(list_nfrs, message):
    for key in list_nfrs:
        if key in message:
            return True
    return False


def _return_nfr_keyword_in_list(list_nfrs, message):
    has_nfr = False
    list_keys = []
    for key in list_nfrs:
        if key in message:
            has_nfr = True
            list_keys.append(key)
    return has_nfr, list_keys


def get_nfrs(message):
    """Return the list of NFRs words and the total number of keywords in the message"""
    nfr_list = {}

    nfr_list['all'], nfr_list['n_all'] = _find_in_list(all_keywords, message)
    nfr_list["maintainability"], nfr_list["n_maint"] = _find_in_list(maint_keywords, message)
    nfr_list["security"], nfr_list["n_sec"] = _find_in_list(security_keywords, message)
    nfr_list["performance"], nfr_list["n_perf"] = _find_in_list(perf_keywords, message)
    nfr_list["robustness"], nfr_list["n_robu"] = _find_in_list(robu_keywords, message)

    nfr_list["n_total"] = nfr_list["n_maint"] + nfr_list["n_sec"] + nfr_list["n_perf"] + nfr_list["n_robu"]

    if nfr_list["n_maint"] == nfr_list["n_sec"] == nfr_list["n_perf"] == nfr_list["n_robu"] == 0:
        nfr_list["has_nfr"] = False
    else:
        nfr_list["has_nfr"] = True

    return nfr_list


def has_nfr(message, nfrs_to_verify):
    """Check whether there is a NFR rin the message"""
    if "Robustness" in nfrs_to_verify and _has_nfr_in_list(robu_keywords, message):
        return True

    if "Maintainability" in nfrs_to_verify and _has_nfr_in_list(maint_keywords, message):
        return True

    if "Security" in nfrs_to_verify and _has_nfr_in_list(security_keywords, message):
        return True

    if "Performance" in nfrs_to_verify and _has_nfr_in_list(perf_keywords, message):
        return True

    return False


def get_nfr_count(message):
    """Collect the number of keywords for each type"""
    nfr_list = {}

    nfr_list["n_maint"] = _find_in_list(maint_keywords, message)[1]
    nfr_list["n_sec"] = _find_in_list(security_keywords, message)[1]
    nfr_list["n_perf"] = _find_in_list(perf_keywords, message)[1]
    nfr_list["n_robu"] = _find_in_list(robu_keywords, message)[1]

    return nfr_list["n_maint"], nfr_list["n_sec"], nfr_list["n_perf"], nfr_list["n_robu"]


def return_nfr_keyword(message):
    """Returns all the keywords and if the message has a general NFR"""
    has_nfr = False
    keywords = []

    if _return_nfr_keyword_in_list(maint_keywords, message)[0]:
        has_nfr = True
        keywords.append(_return_nfr_keyword_in_list(maint_keywords, message)[1])

    if _return_nfr_keyword_in_list(security_keywords, message)[0]:
        has_nfr = True
        keywords.append(_return_nfr_keyword_in_list(security_keywords, message)[1])

    if _return_nfr_keyword_in_list(perf_keywords, message)[0]:
        has_nfr = True
        keywords.append(_return_nfr_keyword_in_list(perf_keywords, message)[1])

    if _return_nfr_keyword_in_list(robu_keywords, message)[0]:
        has_nfr = True
        keywords.append(_return_nfr_keyword_in_list(robu_keywords, message)[1])

    return has_nfr, keywords