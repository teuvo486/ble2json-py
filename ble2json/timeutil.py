import re
from flask import abort
from datetime import date, time, datetime, timedelta

ALIASES = ["epoch", "now", "day", "week", "month", "year"]


def get_timedelta(d):
    return timedelta(
        days=d.get("days", 0),
        seconds=d.get("seconds", 0),
        microseconds=d.get("microseconds", 0),
        milliseconds=d.get("milliseconds", 0),
        minutes=d.get("minutes", 0),
        hours=d.get("hours", 0),
        weeks=d.get("weeks", 0),
    )


def get_datetimes(start, end):
    if not start:
        start = resolve_alias("epoch")
    elif start in ALIASES:
        start = resolve_alias(start)
    else:
        start = validatetime(start)

    if not end:
        end = resolve_alias("now")
    elif end in ALIASES:
        end = resolve_alias(end)
    else:
        end = validatetime(end)

    return start, end


def resolve_alias(a):
    if a == "epoch":
        return "1970-01-01T00:00:00Z"

    if a == "now":
        return datetime.now().isoformat(timespec="seconds")

    if a == "day":
        d = date.today()
    elif a == "week":
        d = date.today() - timedelta(days=date.today().weekday() % 7)
    elif a == "month":
        d = date.today().replace(day=1)
    else:
        d = date.today().replace(day=1, month=1)

    return datetime.combine(d, time()).isoformat(timespec="seconds")
    
    
def validatetime(s):
    if not re.match("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$", s, re.A):
        abort(400)
    
    return s

    
