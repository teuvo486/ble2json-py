import struct
from .util import field, sign_and_magnitude

FMT = ">BBBBHhhhH"

COLS = "humidity,temperature,pressure,accelerationX,accelerationY,accelerationZ,voltage"


def from_bytes(buf):
    t = struct.unpack(FMT, buf)
    return {
        "humidity": field(t[1], 200, lambda v: v * 0.5),
        "temperature": sign_and_magnitude(t[2], t[3]),
        "pressure": field(t[4], 65534, lambda v: v + 50000),
        "accelerationX": field(t[5], -32767, lambda v: v * 0.001),
        "accelerationY": field(t[6], -32767, lambda v: v * 0.001),
        "accelerationZ": field(t[7], -32767, lambda v: v * 0.001),
        "voltage": field(t[8], 3646, lambda v: v * 0.001),
    }
