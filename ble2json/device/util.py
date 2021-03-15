from datetime import date, time, datetime, timedelta

ALIASES = ["epoch", "now", "day", "week", "month", "year"]


def get_datetimes(start, end):
    if not start:
        start = resolve_alias("epoch")
    elif start in ALIASES:
        start = resolve_alias(start)

    if not end:
        end = resolve_alias("now")
    elif end in ALIASES:
        end = resolve_alias(end)

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


def clamp(a, b):
    if (b < 0 and a >= b) or (b > 0 and a <= b):
        return a


def field(a, b, then):
    val = clamp(a, b)

    if val is not None:
        return round(then(val), 3)


def sign_and_magnitude(intg, fract):
    if fract > 100:
        return None

    val = (intg & 0x7F) + fract * 0.01

    if intg & 0x80 == 0:
        return val

    return -val
