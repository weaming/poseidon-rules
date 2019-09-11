import os
from dictate import retrieve_dict


def get_dict_value(data, path):
    try:
        rv = retrieve_dict(data, path)
    except KeyError:
        return None
    if os.getenv("DEBUG"):
        print("{0:>50}".format(path), "=>", "{:>20}".format(str(type(rv))), rv)
    return rv


g = get_dict_value
