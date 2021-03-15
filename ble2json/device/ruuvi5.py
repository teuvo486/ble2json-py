import struct
from .util import clamp, field

FMT = ">BhHHhhhHBHBBBBBB"

COLS = "temperature,humidity,pressure,accelerationX,accelerationY,accelerationZ,voltage,txPower,movementCounter,measurementSequence"


def from_bytes(buf):
    t = struct.unpack(FMT, buf)
    return {
        "temperature": field(t[1], -32767, lambda v: v * 0.005),
        "humidity": field(t[2], 40000, lambda v: v * 0.0025),
        "pressure": field(t[3], 65534, lambda v: v + 50000),
        "accelerationX": field(t[4], -32767, lambda v: v * 0.001),
        "accelerationY": field(t[5], -32767, lambda v: v * 0.001),
        "accelerationZ": field(t[6], -32767, lambda v: v * 0.001),
        "voltage": field(t[7] >> 5, 2046, lambda v: v * 0.001 + 1.6),
        "txPower": field(t[7] & 0x1F, 30, lambda v: v * 2 - 40),
        "movementCounter": clamp(t[8], 254),
        "measurementSequence": clamp(t[9], 65534),
    }
