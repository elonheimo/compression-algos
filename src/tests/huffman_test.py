import unittest
from bitarray import bitarray
from huffman.huffman import HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):
    def make_test_bitarray(self) -> bitarray:
        #        / \
        #      /\   /\
        #    /\  c d  e
        #   a  b
        testbuffer = bitarray('0001')
        testbuffer.frombytes(str.encode("A"))
        testbuffer.append(1)
        testbuffer.frombytes(str.encode("B"))
        testbuffer.append(1)
        testbuffer.frombytes(str.encode("C"))
        testbuffer.extend([0,1])
        testbuffer.frombytes(str.encode("D"))
        testbuffer.append(1)
        testbuffer.frombytes(str.encode("E"))
        return testbuffer

    def make_test_tree(self) -> HuffmanCoding.TreeNode:
        huffman_coding = HuffmanCoding("","")
        root = huffman_coding.TreeNode(None, 0)
        root.left = huffman_coding.TreeNode(None, 0)
        root.left.left = huffman_coding.TreeNode(None, 0)
        root.left.left.left = huffman_coding.TreeNode(
            int.from_bytes(str.encode("A"), byteorder='big'), 0
        )
        root.left.left.right = huffman_coding.TreeNode(
            int.from_bytes(str.encode("B"), byteorder='big'), 0
        )
        root.left.right = huffman_coding.TreeNode(
            int.from_bytes(str.encode("C"), byteorder='big'), 0
        )
        root.right = huffman_coding.TreeNode(None, 0)
        root.right.left = huffman_coding.TreeNode(
            int.from_bytes(str.encode("D"), byteorder='big'), 0
        )
        root.right.right = huffman_coding.TreeNode(
            int.from_bytes(str.encode("E"), byteorder='big'), 0
        )
        return root

    def test__str__(self):
        self.assertEqual(
            isinstance(str(self.make_test_tree()), str),
            True
        )
    def test_encode(self):
        input_path = "samples/munkki_kammio.txt"
        encoded = "testing_files/munkki_kammio.txt.hc"
        decoded = "testing_files/munkki_kammio_hc.txt"
        HuffmanCoding(input_path, encoded).encode()
        HuffmanCoding(encoded, decoded).decode()
        with open(input_path, "rb") as original, open(decoded, "rb") as new:
            original_str = original.read()
            new_str = new.read()
            self.assertEqual(original_str, new_str)

    def test_huffman_codes(self):
        huffman_coding = HuffmanCoding("","")
        byte_to_code_dict = huffman_coding.huffman_codes(
            self.make_test_tree()
        )
        self.assertEqual(
            byte_to_code_dict[int.from_bytes(str.encode("A"), byteorder='big')],
            bitarray('111')
        )

    def test_tree_to_bitarray(self):
        huffman_coding = HuffmanCoding("","")

        self.assertEqual(
            self.make_test_bitarray(),
            huffman_coding.tree_to_bitarray(
                self.make_test_tree()
            )
        )

    def test_header_to_binarytree(self):
        huffman_coding = HuffmanCoding("","")
        og_test_buffer = self.make_test_bitarray()
        test_buffer_with_tail_bits = og_test_buffer + bitarray('01110')
        (root_from_test_buffer, index) = huffman_coding.header_to_binarytree(test_buffer_with_tail_bits, 0)
        new_buffer = huffman_coding.tree_to_bitarray(root_from_test_buffer)
        self.assertEqual(
            og_test_buffer,
            new_buffer
        )

    def test_encoded_tail_length(self):
        data = bitarray('11100000')
        huffman_coding = HuffmanCoding("","")
        self.assertEqual(
            huffman_coding.encoded_tail_length(data),
            7
        )
