from collections import defaultdict
import heapq
from bitarray import bitarray


class HuffmanCoding:
    def __init__(self, input_path :str, output_path :str) -> None:
        """Class that encodes and decodes files with Huffman coding

        Args:
            input_path (str): 
            output_path (str):
        """
        self.input_file_path = input_path
        self.output_file_path = output_path

    class TreeNode:
        def __init__(self, content :bytes, frequency :int) -> None:
            self.content = content
            self.frequency = frequency
            self.left, self.right = None, None

        def __lt__(self, other):
            if self.frequency < other.frequency:
                return True
            return False

        def __str__(self) -> str:
            ret = "\n"
            def loop_layers(node, level) ->str:
                if node.left:
                    loop_layers(node.left, level+1)

                nonlocal ret
                ret += (' ' * 4 * level + '-> ' + str(node.content)+ "\n")
                
                if node.right:
                    loop_layers(node.right, level+1)
            loop_layers(self, 0)
            return ret
                
                

    def frequency_dict(self, byte_list :list) -> dict:
        """Creates dictionary with keys as bytes and values as their count

        Args:
            byte_list (list): list of bytes represented as ints

        Returns:
            dict: _description_
        """
        freq_dict = defaultdict(lambda: 0)
        for i in byte_list:
            # note that
            # bytes type of list elements are ints not bytes
            # dict[int] = int
            freq_dict[i] += 1
        return freq_dict

    def create_tree(self, freq_dict :dict) -> TreeNode:
        """Creates binarytree from a dictionary of freaquencies

        Args:
            freq_dict (dict): dict[int] = int

        Returns:
            TreeNode: Root node of binarytree
        """
        heap_list = []
        for key, value in freq_dict.items():
            #key = byte_as_int, value = frequency of byte as int
            node = self.TreeNode(
                key,
                value
            )
            heapq.heappush(heap_list, node)

        while len(heap_list) >1:
            l_child, r_child = heapq.heappop(heap_list), heapq.heappop(heap_list)
            parent = self.TreeNode(
                None,
                l_child.frequency + r_child.frequency
            )
            parent.left, parent.right = l_child, r_child

            heapq.heappush(heap_list, parent)
   
        return heap_list[0] # returns root node

    def huffman_codes(self, root: TreeNode) -> dict:
        """Creates dictionary of every databyte to unique Huffman code

        Args:
            root (TreeNode): root node

        Returns:
            dict: dict[int] = bitarray
        """
        byte_to_code_dict = {}

        def dict_filler(parent, code :bitarray):
            if parent.content: #achieved leaf node
                byte_to_code_dict[parent.content] = code
                return
            dict_filler(
                parent.left,
                code + bitarray('1')
            )
            dict_filler(
                parent.right,
                code + bitarray('0')
            )
        dict_filler(
            root,
            bitarray(endian='big')
        )

        return byte_to_code_dict
    
    def tree_to_bitarray(self, root :TreeNode) -> bitarray:
        """Generates bitarray representing huffman tree

        Args:
            root (TreeNode): root node

        Returns:
            bitarray
        """
        route_buffer = bitarray('')
        def helper(node):
            if node is None:
                return
            if node.content:
                route_buffer.append(1)
                route_buffer.frombytes(
                    node.content.to_bytes(1, byteorder='big')
                )
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

    def header_to_binarytree(self, data :bitarray, start_index: int) -> tuple:
        """Creates binary tree of huffman codes from binary representing it

        Args:
            data (bitarray): data
            start_index (int): part of header where binary tree starts

        Returns:
            tuple: (root, index) root node of binary tree and index is the last bit of header
        """
        def helper(node, i):
            if data[i] == 0:
                node.left = self.TreeNode(None, 0)
                i = helper(
                    node.left, i + 1
                )
                node.right = self.TreeNode(None, 0)
                i = helper(
                    node.right, i + 1
                )
            elif data[i] == 1:
                #read one byte
                i += 1
                node.content = data[i: i+8].tobytes()[0]
                i += 7
            return i

        root= self.TreeNode(None, 0)
        index = helper(root, start_index)
        return (root, index)


    def encode(self):
        """Encodes input file with huffman coding and saves to outputfile
        """
        input_data = self.read_input()
        freq_dict = self.frequency_dict(input_data)
        root_node = self.create_tree(freq_dict)
        huffman_codes = self.huffman_codes(root_node)
        temp_buffer = self.tree_to_bitarray(root_node)
        # buffer
        # |huffmancodes|
        for byte_as_int in input_data:
            temp_buffer.extend(
                huffman_codes[byte_as_int]
            )
        # buffer
        # |huffmancodes|encoded bytes|
        tail_bits = (
            8 -
            ((len(temp_buffer) +3 ) % 8)
        )
        if tail_bits == 8:
            tail_bits = 0
        final_bitarray = bitarray('')
        final_bitarray.frombytes(
            bytes([tail_bits])
        )
        final_bitarray = final_bitarray[5:]
        final_bitarray += temp_buffer
        final_bitarray.fill() #add tail bits
        # buffer
        # 0 bits amount|huffmancodes|encoded bytes|0bits
        self.save_output(
            final_bitarray.tobytes()
        )
    
    def encoded_tail_length(self, data: bitarray) -> int:
        """Returns the tail length of encoded data as int

        Args:
            data (bitarray): data

        Returns:
            int: length of tail bits to ignore
        """
        discard_tail_bits = bitarray('00000')
        discard_tail_bits += data[:3]
        return int.from_bytes(
            discard_tail_bits.tobytes(),
            'big'
        )

    def decode(self):
        """Decodes input_file and saves as outputfile
        """
        data = bitarray('')
        data.frombytes(
            self.read_input()
        )
        tail_length = self.encoded_tail_length(data)
        (root, index) = self.header_to_binarytree(data, 3 )
        index += 1
        buffer = []#[bytearray()]
        current_node = root
        while index < len(data) - tail_length:
            if data[index] == 1:
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.content:
                buffer.append(current_node.content)
                current_node = root
            index += 1
        self.save_output(bytes(buffer))

    def save_output(self, buffer: bytes):
        """Saves data

        Args:
            buffer (bytes): data to save
        """
        try:
            # wb = write binary
            with open(self.output_file_path, 'wb') as output_file:
                output_file.write(buffer)
            print(f"Succesfully saved {self.output_file_path}")
        except IOError:
            print("Error while saving output {file_path}")


    def read_input(self) -> bytes:
        """Read objects input file

        Returns:
            bytes: data as bytes
        """
        try:
            # rb = read binary
            with open(self.input_file_path, 'rb') as input_file:
                return input_file.read()
        except IOError:
            return print(f"could not open {self.input_file_path}")
        