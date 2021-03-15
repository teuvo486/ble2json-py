import unittest
from ble2json.device.ruuvi5 import from_bytes


class TestRuuvi5(unittest.TestCase):
    valid_in = b"\x05\x12\xFC\x53\x94\xC3\x7C\x00\x04\xFF\xFC\x04\x0C\xAC\x36\x42\x00\xCD\xCB\xB8\x33\x4C\x88\x4F"

    valid_out = {
        "temperature": 24.3,
        "humidity": 53.49,
        "pressure": 100044.0,
        "accelerationX": 0.004,
        "accelerationY": -0.004,
        "accelerationZ": 1.036,
        "voltage": 2.977,
        "txPower": 4.0,
        "movementCounter": 66,
        "measurementSequence": 205,
    }

    max_in = b"\x05\x7F\xFF\x9c\x40\xFF\xFE\x7F\xFF\x7F\xFF\x7F\xFF\xFF\xDE\xFE\xFF\xFE\xCB\xB8\x33\x4C\x88\x50"

    max_out = {
        "temperature": 163.835,
        "humidity": 100.0,
        "pressure": 115534.0,
        "accelerationX": 32.767,
        "accelerationY": 32.767,
        "accelerationZ": 32.767,
        "voltage": 3.646,
        "txPower": 20.0,
        "movementCounter": 254,
        "measurementSequence": 65534,
    }

    min_in = b"\x05\x80\x01\x00\x00\x00\x00\x80\x01\x80\x01\x80\x01\x00\x00\x00\x00\x00\xCB\xB8\x33\x4C\x88\x51"

    min_out = {
        "temperature": -163.835,
        "humidity": 0.0,
        "pressure": 50000.0,
        "accelerationX": -32.767,
        "accelerationY": -32.767,
        "accelerationZ": -32.767,
        "voltage": 1.6,
        "txPower": -40.0,
        "movementCounter": 0,
        "measurementSequence": 0,
    }

    invalid_in = b"\x05\x80\x00\xFF\xFF\xFF\xFF\x80\x00\x80\x00\x80\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    invalid_out = {
        "temperature": None,
        "humidity": None,
        "pressure": None,
        "accelerationX": None,
        "accelerationY": None,
        "accelerationZ": None,
        "voltage": None,
        "txPower": None,
        "movementCounter": None,
        "measurementSequence": None,
    }

    def test_valid(self):
        self.assertEqual(from_bytes(self.valid_in), self.valid_out)

    def test_max(self):
        self.assertEqual(from_bytes(self.max_in), self.max_out)

    def test_min(self):
        self.assertEqual(from_bytes(self.min_in), self.min_out)

    def test_invalid(self):
        self.assertEqual(from_bytes(self.invalid_in), self.invalid_out)


if __name__ == "__main__":
    unittest.main()
