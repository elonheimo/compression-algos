import unittest

from lz.lempelziv import LZ77

class TestLZ77(unittest.TestCase):
    def setUp(self) -> None:
        self.input = "samples/The_Count_of_Monte_Cristo_by_Dumas.txt"
        self.encoded = "testing_files/The_Count_of_Monte_Cristo_by_Dumas.txt.lz"
        self.decoded = "testing_files/The_Count_of_Monte_Cristo_by_Dumas.txt"
        return super().setUp()

    def test_encode(self):
        LZ77(self.input, self.encoded).encode

    def test_decode(self):
        LZ77(self.encoded, self.decoded).decode
        with open(self.input) as original, open(self.decoded) as new:
            self.assertEqual(
                str(original.read()),
                str(new.read())
            )

