import argparse
import sys
from lz.lempel_ziv import LZ77


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-lz', action='store_true')
    parser.add_argument('-hc', action='store_true')
    parser.add_argument('-d', '--decode', action='store_true')

    args = parser.parse_args()

    if not args.lz and not args.hc:
        print("No algorithm specified")
        sys.exit(-1)

    if args.decode:
        if args.lz:
            LZ77(
                args.input,
                args.output
            ).decode()
    else: #encode
        if args.lz:
            LZ77(
                args.input,
                args.output
            ).encode()
 