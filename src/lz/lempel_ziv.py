from sys import byteorder
from bitarray import bitarray
from bitarray.util import ba2int, make_endian
from tqdm import tqdm
from . sa import MatchFinder


class LZ77:
    def __init__(self, input_file_path: str, output_file_path: str):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def encode(self):
        self.input_data = self.read_input()
        match_finder = MatchFinder(self.input_data)
        buffer = bitarray(endian='big')
        index = 0
        progress_bar = tqdm(total = len(self.input_data))
        while index < len(self.input_data):
            match = match_finder.find_longest_match(index)
            if match:
                buffer.append(1)  # flag bit
                (dist, length) = match
                
                dist_bits = bitarray(endian='little')
                dist_bits.frombytes(
                    int(dist).to_bytes(length=2, byteorder='little')
                )
                dist_bits = dist_bits[:12]
                buffer.extend(dist_bits)
                
                length_bits = bitarray(endian='little')
                length_bits.frombytes(
                    int(length).to_bytes(length=1, byteorder='little')
                )
                length_bits = length_bits[:4]
                buffer.extend(length_bits)

                index += length
                progress_bar.update(length)

            else:
                buffer.append(0)  # flag bit
                # character
                buffer.frombytes(bytes([self.input_data[index]]))
                index += 1
                progress_bar.update(1)
        progress_bar.close()

        buffer.fill()  # fills the last byte if not full

        self.save_output(buffer)

    def decode(self):
        data = bitarray(endian='big')
        # data in bits and most significant bit first
        buffer = []

        try:
            with open(self.input_file_path, 'rb') as input_file:
                data.fromfile(input_file)
        except IOError:
            print('Error open while decompress')
            raise
        
        i = 0
        while i < len(data)-8:
            flag = data[i]
            i += 1

            if flag == 0:
                # append one byte
                buffer.extend(
                    data[i: i+8].tobytes()
                )
                i += 8

            else:  # flag == 1

                relative_distance = ba2int(
                    make_endian(data[i : i+12], endian='little')
                )
                i += 12
                length = ba2int(
                    make_endian(data[i : i+4], endian='little')
                )
                i += 4

                for len_i in range(length):
                    buffer.append(
                        buffer[-relative_distance]
                    )
        output_byte_data = bytes(buffer)

        with open(self.output_file_path, "wb") as f:
            f.write(output_byte_data)
            f.close()

    def read_input(self) -> bytes:
        try:
            # rb = read binary
            with open(self.input_file_path, 'rb') as input_file:
                return input_file.read()
        except IOError:
            print(f"could not open {self.input_file_path}")

    def save_output(self, buffer):
        try:
            # wb = write binary
            with open(self.output_file_path, 'wb') as output_file:
                output_file.write(buffer.tobytes())
            print(f"Succesfully saved {self.output_file_path}")
        except IOError:
            print("Error while saving output {file_path}")
