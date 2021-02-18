import unittest
from ble2json.device.ruuvi5 import from_bytes


class TestRuuvi5(unittest.TestCase):

    valid_in = b"\x05\x12\xFC\x53\x94\xC3\x7C\x00\x04\xFF\xFC\x04\x0C\xAC\x36\x42\x00\xCD\xCB\xB8\x33\x4C\x88\x4F"
    valid_out = (24.3, 53.49, 100044.0, 0.004, -0.004, 1.036, 2.977, 4.0, 66, 205)

    max_in = b"\x05\x7F\xFF\x9c\x40\xFF\xFE\x7F\xFF\x7F\xFF\x7F\xFF\xFF\xDE\xFE\xFF\xFE\xCB\xB8\x33\x4C\x88\x50"
    max_out = (
        163.835,
        100.0,
        115534.0,
        32.767,
        32.767,
        32.767,
        3.646,
        20.0,
        254,
        65534,
    )

    min_in = b"\x05\x80\x01\x00\x00\x00\x00\x80\x01\x80\x01\x80\x01\x00\x00\x00\x00\x00\xCB\xB8\x33\x4C\x88\x51"
    min_out = (-163.835, 0.0, 50000.0, -32.767, -32.767, -32.767, 1.6, -40.0, 0, 0)

    invalid_in = b"\x05\x80\x00\xFF\xFF\xFF\xFF\x80\x00\x80\x00\x80\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
    invalid_out = (None, None, None, None, None, None, None, None, None, None)

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
