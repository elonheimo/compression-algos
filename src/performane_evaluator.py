import csv
import os 
import random
import string
import time
from huffman.huffman import HuffmanCoding
from lz.lempel_ziv import LZ77

__n_bytes= [
    100,
    100_000,
    1_000_000
]


def start_performance_eval():
    if not os.path.exists("temp"):
        os.makedirs(f"{os.getcwd()}/temp")
    inputs, outputs = sample_paths()
    print(inputs, outputs)
    print("generating random files")
    rand_inputs, rand_outputs = generate_rand_byte_files()
    inputs.extend(rand_inputs)
    outputs.extend(rand_outputs)
    print("start evaluations")
    rows = time_encode_decode(inputs, outputs)
    write_to_csv(rows)
    print(*rows, sep="\n")

def sample_paths():
    inputs = os.listdir("samples")
    outputs = []
    for i in range(len(inputs)):
        outputs.append(f"{os.getcwd()}/temp/{inputs[i]}")
        inputs[i] = f"{os.getcwd()}/samples/{inputs[i]}"
    return (inputs, outputs)

def write_to_csv(rows):
    with open("temp/performance_results.csv","a+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

def generate_rand_byte_file(size, filename):
    chars = ''.join(
        [random.choice(string.printable) for i in range(size)]
    )
    with open(filename, 'w') as f:
        f.write(chars)
        f.close()

def generate_rand_byte_files():
    input_paths = []
    output_paths = []
    for size in __n_bytes:
        input_path = f"{os.getcwd()}/temp/{str(size)}_input.txt"
        output_path = f"{os.getcwd()}/temp/{str(size)}_output.txt"
        generate_rand_byte_file(
            size,
            input_path
        )
        input_paths.append(input_path)
        output_paths.append(output_path)
    return (
        input_paths,
        output_paths
    )


def time_encode_decode(input_paths: list, output_paths: list):
    rows = []
    for (i, input_path) in enumerate(input_paths):
        print(i, input_path, output_paths[i], "enum")
        rows.extend(
            encode_decode(
                input_path,
                output_paths[i]
            )
        )
    return rows

def encode_decode(input_path: str, output_path: str):
    rows = []
    print(
        [
            input_path, f"{output_path}.hc"
        ], [
            f"{output_path}.hc", output_path
        ]
    )
    compressors = [
        (   
            HuffmanCoding(input_path, f"{output_path}.hc"),
            HuffmanCoding(f"{output_path}.hc", output_path)
        ),
        (   
            LZ77(input_path, f"{output_path}.lz"),
            LZ77(f"{output_path}.lz", output_path)
        )
    ]
    algo_names = ["Huffman", "lempel-ziv"]
    for i, ele in enumerate(compressors):
        #| file        | algo         |encode time(s)|decode time(s)|size(KB)      | compressed size(KB)|space saving|
        row = [
            input_path.split("/")[-1],
            algo_names[i]
        ]
        encoder, decoder = ele
        start_encode = time.time()
        encoder.encode()
        start_decode = time.time()
        decoder.decode()
        end_decode= time.time()
        #encode time
        row.append(
            str(round(start_decode-start_encode,6))
        )
        #decode time
        row.append(
            str(round(end_decode-start_decode,6))
        )
        #size
        row.append(
            str(
                os.path.getsize(encoder.input_file_path)
            )
        )
        #compressed size
        row.append(
            str(
                os.path.getsize(encoder.output_file_path)
            )
        )
        #space saving
        row.append(
            str(round(1- int(row[-2]) / int(row[-1]),3)*100) + "%"
        )
        del encoder
        del decoder
        rows.append(row)
    return rows


if __name__ == '__main__':
    start_performance_eval()
