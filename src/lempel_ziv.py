from sa import *
from bitarray import bitarray
from sa import MatchFinder

class lz77:
    def __init__(self, input_file_path: str, output_file_path: str):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def compress(self):
        self.input_data = self.read_input()
        self.mf = MatchFinder(self.input_data)
        buffer = bitarray(endian='big')
        index = 0
        while index < len(self.input_data):
            if index % 10000 == 0: print(index)
            match = self.mf.findLongestMatch(index)

            if match:
                (dist, length) = match
                buffer.append(True)
                buffer.frombytes(bytes([dist >> 4]))
                buffer.frombytes(bytes([((dist & 0xf) << 4) | length]))
                index += length

            else:
                buffer.append(False)
                buffer.frombytes(bytes([self.input_data[index]]))
                index += 1

        buffer.fill() #fills the last byte if not full

        self.save_output(buffer)

    def ddecompress(self):
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
                #append one byte
                buffer.extend(
                    data[i: i+8].tobytes()
                )
                i += 8

            else: # flag == 1
                byte1 = int.from_bytes(data[i: i+8], "big")
                i += 8
                byte2 = int.from_bytes(data[i: i+8], "big")
                i += 8

                # Example for bitwise operations
                # byte1 00000001 byte2 11111111
                # AFTER BITWISE SHIFTS 
                # byte1 000000010000 byte2 00001111
                # AFTER BITWISE OR |
                # 000000011111

                relative_distance = (
                    (byte1 << 4)
                    |
                    (byte2 >> 4)
                )

                # BITWISE AND &
                # only 4 last bits
                length = (byte2 & 15)
                for len_i in range(length):
                    buffer.append(
                        buffer[-relative_distance]
                    )
                """
                buffer.extend(
                    buffer[ -relative_distance: -relative_distance + length]
                )
                """
        
        output_byte_data = bytes(buffer)
        print(output_byte_data)

        with open(self.output_file_path, "wb") as f:
            f.write(output_byte_data)
            f.close()

    def read_input(self) -> bytes:
        try:
            # rb = read binary
            with open(self.input_file_path, 'rb') as input_file:
                return input_file.read()
        except IOError:
            print("could not open {file_path}")

    def save_output(self, buffer):
        try:
            # wb = write binary
            with open(self.output_file_path, 'wb') as output_file:
                output_file.write(buffer.tobytes())
            print(f"Succesfully saved {self.output_file_path}")
        except IOError:
            print("Error while saving output {file_path}")
    