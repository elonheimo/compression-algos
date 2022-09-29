from bitarray import bitarray
from . sa import MatchFinder


class LZ77:
    def __init__(self, input_file_path: str, output_file_path: str):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.input_data = self.read_input()
        self.match_finder = MatchFinder(self.input_data)

    def encode(self):
        buffer = bitarray(endian='big')
        index = 0
        while index < len(self.input_data):
            if index % 10000 == 0:
                print(index)
            match = self.match_finder.find_longest_match(index)

            if match:
                buffer.append(1)  # flag bit
                (dist, length) = match
                # dist is 12bits so BITWISE SHIFT right 4
                byte1 = bytes([dist >> 4])
                buffer.frombytes(byte1)
                # BITWISE AND to leave 4 smallest bits
                # shift left and BITWISE OR to add length (4bits)
                byte2 = bytes([
                    ((dist & 15) << 4)
                    | length
                ])
                buffer.frombytes(byte2)
                index += length

            else:
                buffer.append(0)  # flag bit
                # character
                buffer.frombytes(bytes([self.input_data[index]]))
                index += 1

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
