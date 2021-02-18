def clamp(a, b):
    if (b < 0 and a < b) or (b > 0 and a > b):
        return None
    else:
        return a


def field(a, b, then):
    val = clamp(a, b)
    if val is not None:
        return round(then(val), 3)
    else:
        return None


def sign_and_magnitude(intg, fract):
    if fract > 100:
        return None

    val = (intg & 0x7F) + fract * 0.01

    if intg & 0x80 == 0:
        return val
    else:
        return -val
