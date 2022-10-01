from collections import defaultdict
import heapq
from bitarray import bitarray


class HuffmanCoding:
    def __init__(self, input_path :str, output_path :str) -> None:
        self.input_file_path = input_path
        self.output_file_path = output_path

    class TreeNode:
        def __init__(self, content :bytes, frequency :int) -> None:
            self.content = content
            self.frequency = frequency
            self.left, self.right = None, None

        def __lt__(self, other):
            if self.frequency < other.frequency:
                return False
            return True


    def frequency_dict(self, byte_list :list):
        freq_dict = defaultdict(lambda: 0)
        for i in byte_list:
            freq_dict[i] += 1
        return freq_dict

    def create_tree(self, freq_dict :dict) -> TreeNode:
        heap_list = []
        for key, value in freq_dict.items():
            #key = byte, value = int
            node = self.TreeNode(key, value)
            heapq.heappush(heap_list, node)

        while len(heap_list) >1:
            l_child, r_child = heapq.heappop(heap_list), heapq.heappop(heap_list)
            parent = self.TreeNode(
                None,
                l_child.frequency + r_child.frequency
            )
            parent.left, parent.right = l_child, r_child

            heapq.heappush(heap_list, parent)
   
        return heap_list[1] # returns root node

    def huffman_codes(self, root: TreeNode):
        byte_to_code_dict = {}

        def dict_filler(parent, code :bitarray):
            if not parent:
                return
            if parent.content: #achieved leaf node
                byte_to_code_dict[parent.content] = code
                return
            dict_filler(
                parent.left,
                code + bitarray('0')
            )
            dict_filler(
                parent.right,
                code + bitarray('1')
            )
        dict_filler(
            root,
            bitarray(endian='big')
        )

        return byte_to_code_dict

    def read_input(self) -> bytes:
        try:
            # rb = read binary
            with open(self.input_file_path, 'rb') as input_file:
                return input_file.read()
        except IOError:
            return print(f"could not open {self.input_file_path}")
    
    def tree_to_bitarray(self, root :TreeNode) -> bitarray:
        route_buffer = bitarray('')
        def helper(node):
            if node is None:
                return
            if node.content:
                route_buffer.append(1)
                route_buffer.frombytes(node.content)
            else:
                route_buffer.append(0)
            helper(
                node.left
            )
            helper(
                node.right
            )
        helper(root)
        return route_buffer

    def encode(self):
        input_data = self.read_input()
        freq_dict = self.frequency_dict(input_data)
        root_node = self.create_tree(freq_dict)
        huffman_codes = self.huffman_codes(root_node)
        buffer = self.tree_to_bitarray(root_node)
        for byte in input_data:
            buffer += huffman_codes[byte]
        