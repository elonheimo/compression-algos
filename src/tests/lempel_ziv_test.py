import unittest
from lz.lempel_ziv import LZ77

class TestLZ77(unittest.TestCase):
    def setUp(self) -> None:
        self.input = "samples/munkki_kammio.txt"
        self.encoded = "testing_files/munkki_kammio.txt.lz"
        self.decoded = "testing_files/munkki_kammio.txt"
        return super().setUp()

    def test_encode(self):
        LZ77(self.input, self.encoded).encode()
        
    def test_decode(self):
        LZ77(self.encoded, self.decoded).decode()
        with open(self.input, "rb") as original, open(self.decoded, "rb") as new:
            original_str = original.read()
            new_str = new.read()
            self.assertEqual(original_str, new_str)

