from array import array
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
    print("generating files with random bytes")
    rand_inputs, rand_outputs = generate_rand_byte_files()
    inputs.extend(rand_inputs)
    outputs.extend(rand_outputs)
    print("start evaluations")
    rows = measure_preformances(inputs, outputs)
    write_to_csv(rows)
    print(*rows, sep="\n")

def sample_paths() -> tuple:
    """Scans samples folder for files

    Returns:
        tuple: (inputs, outputs)
        2 arrays in a tuple. Arrays contain input and output paths in order.

    """
    inputs = os.listdir("samples")
    outputs = []
    ## pylint: disable= consider-using-enumerate
    for i in range(len(inputs)):
        outputs.append(f"{os.getcwd()}/temp/{inputs[i]}")
        inputs[i] = f"{os.getcwd()}/samples/{inputs[i]}"
    return (inputs, outputs)

def write_to_csv(rows):
    """Writes the performance test results to csv-file.

    Args:
        rows : Two dimentional array containing performance result data
    """
    with open("temp/performance_results.csv","w", encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

def generate_rand_byte_file(size, filename):
    chars = ''.join(
        [random.choice(string.printable) for i in range(size)]
    )
    with open(filename, 'w', encoding='utf-8') as rand_byte_file:
        rand_byte_file.write(chars)
        rand_byte_file.close()

def generate_rand_byte_files() -> tuple:
    """Generates files to /temp folder filled with random bytes.

    Returns:
        tuple: (inputs, outputs)
        2 arrays in a tuple. Arrays contain input and output paths in order.
    """
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


def measure_preformances(input_paths: list, output_paths: list) -> array:
    """Loops through all input_files and measures performance.

    Args:
        input_paths (list): list of input paths 
        output_paths (list): list of output paths

    Returns:
        array: two dimensional array of string to convert to save as .csv file
    """
    rows = []
    rows.append([
        "file name",
        "algorithm",
        "encode time (s)",
        "decode time (s)",
        "size (KB)",
        "compressed size(KB)",
        "space saved (%)"
    ])
    for (i, input_path) in enumerate(input_paths):
        rows.extend(
            encode_decode(
                input_path,
                output_paths[i]
            )
        )
    return rows

def encode_decode(input_path: str, output_path: str) -> array:
    """Performs encodes the input file and decodes. 
    Measures time and file size and saves results to an array.

    Args:
        input_paths (list): list of input paths
        output_paths (list): list of output paths

    Returns:
        array: two dimensional array of string to convert to save as .csv file
    """
    rows = []
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
        #row structure
        #|file name|algorithm |encode time (s)|decode time (s)|size (KB)|compressed size(KB)|space saved (%)|
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
            str(round(100- int(row[-1]) / int(row[-2])*100,3)) + "%"
        )
        del encoder
        del decoder
        rows.append(row)
    return rows


if __name__ == '__main__':
    start_performance_eval()
