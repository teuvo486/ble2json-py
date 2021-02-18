import unittest
from ble2json.device.ruuvi3 import from_bytes


class TestRuuvi3(unittest.TestCase):

    valid_in = b"\x03\x29\x1A\x1E\xCE\x1E\xFC\x18\xF9\x42\x02\xCA\x0B\x53"
    valid_out = (20.5, 26.3, 102766.0, -1.0, -1.726, 0.714, 2.899)

    max_in = b"\x03\xC8\x7F\x63\xFF\xFE\x7F\xFF\x7F\xFF\x7F\xFF\x0E\x3E"
    max_out = (100.0, 127.99, 115534.0, 32.767, 32.767, 32.767, 3.646)

    min_in = b"\x03\x00\xFF\x63\x00\x00\x80\x01\x80\x01\x80\x01\x06\x40"
    min_out = (0.0, -127.99, 50000.0, -32.767, -32.767, -32.767, 1.6)

    invalid_in = b"\x03\xFF\xFF\xFF\xFF\xFF\x80\x00\x80\x00\x80\x00\xFF\xFF"
    invalid_out = (None, None, None, None, None, None, None)

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
