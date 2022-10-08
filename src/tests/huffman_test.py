import unittest
from bitarray import bitarray
from huffman.huffman import HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

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

    def test_tree_to_bitarray(self):
        huffman_coding = HuffmanCoding("","")

        root = huffman_coding.TreeNode(None, 0)
        root.left = huffman_coding.TreeNode(None, 0)
        root.left.left = huffman_coding.TreeNode(None, 0)
        root.left.left.left = huffman_coding.TreeNode(
            str.encode("A"), 0
        )
        root.left.left.right = huffman_coding.TreeNode(
            str.encode("B"), 0
        )
        root.left.right = huffman_coding.TreeNode(
            str.encode("C"), 0
        )
        root.right = huffman_coding.TreeNode(None, 0)
        root.right.left = huffman_coding.TreeNode(
            str.encode("D"), 0
        )
        root.right.right = huffman_coding.TreeNode(
            str.encode("E"), 0
        )
        self.assertEqual(
            self.make_test_bitarray(),
            huffman_coding.tree_to_bitarray(root)
        )

    def test_header_to_binarytree(self):
        huffman_coding = HuffmanCoding("","")
        test_buffer = self.make_test_bitarray()
        root_from_test_buffer = huffman_coding.header_to_binarytree(test_buffer)
        new_buffer = huffman_coding.tree_to_bitarray(root_from_test_buffer)
        self.assertEqual(
            test_buffer,
            new_buffer
        )
