import argparse
import sys
from huffman.huffman import HuffmanCoding
from lz.lempel_ziv import LZ77
from performance_eval import start_performance_eval


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Encode and decode files. Encodes by default")
    parser.add_argument(
        '-i', '--input', type=str,
        help="Define input file path"
    )
    parser.add_argument(
        '-o', '--output', type=str,
        help="Define output file path"
    )
    parser.add_argument(
        '-lz', action='store_true', help="Use lempel-ziv algorithm"
    )
    parser.add_argument(
        '-hc', action='store_true', help="Use Huffman coding algorithm"
    )
    parser.add_argument(
        '-d', '--decode', action='store_true',
        help="Flag to decode specified file"
    )
    parser.add_argument(
        '-p', '--performance_eval', action='store_true',
        help="Runs performance evaluations from /samples folder. Will ignore all other parameters."
    )

    args = parser.parse_args()
    if args.performance_eval:
        start_performance_eval()
        print("Completer performance evaluations")
        sys.exit(-1)
        
    if not args.lz and not args.hc:
        print("No algorithm specified")
        sys.exit(-1)

    if not args.input or not args.output:
        print("Input or output not specified")
        sys.exit(-1)

    if args.decode:
        if args.lz:
            LZ77(
                args.input,
                args.output
            ).decode()
        if args.hc:
            HuffmanCoding(
                args.input,
                args.output
            ).decode()
    else: #encode
        if args.lz:
            LZ77(
                args.input,
                args.output
            ).encode()
        if args.hc:
            HuffmanCoding(
                args.input,
                args.output
            ).encode()
 