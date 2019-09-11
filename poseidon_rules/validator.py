import datetime

DATE_FORMAT = "%Y-%m-%d"


def is_date_format(text, format=DATE_FORMAT):
    try:
        datetime.datetime.strptime(text, format)
        return True
    except Exception:
        return False
