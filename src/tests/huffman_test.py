import unittest
from bitarray import bitarray
from huffman.huffman import HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

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

        ret = huffman_coding.tree_to_bitarray(root)
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
        print(ret)
        self.assertEqual(testbuffer, ret)
