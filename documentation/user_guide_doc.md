# User guide

## Installation

Install [git](https://www.atlassian.com/git/tutorials/install-git) on your system.

Check your local version with ```python3 --version``` 

Install [python](https://realpython.com/installing-python/) version 3.8.10 if not installed.

Clone the github repository

```git clone https://github.com/elonheimo/compression-algos```

Change directory to downloaded folder

Check that you have poetry version 1.2.2 with ```poetry --version```

Install [poetry](https://pypi.org/project/poetry/) if not installed.

Run ```poetry install```

Enter poetry shell
```poetry shell```

Further instructions on use are under command line interface.

## Cli, Command line interface

Execute commands from poetry shell

### Example encode&decode file

Encode


```python3 main.py -i <input file path> -o <output_file_path> <algorithm -lz or -hz>```

```python3 main.py -i temp/100_input.txt -o temp/example.txt.hc -hc```

decode

```python3 main.py -i <input file path> -o <output_file_path> <algorithm -lz or -hz> -d```

```python3 main.py -i temp/example.txt.hc -o temp/example.txt -hc -d```

### Help
```python3 main.py -h```

```
usage: Encode and decode files. Encodes by default [-h] [-i] [-o] [-lz] [-hc] [-d] [-p]

optional arguments:
  -h, --help            show this help message and exit
  -i, --input           Define input file path
  -o, --output          Define output file path
  -lz                   Use lempel-ziv algorithm
  -hc                   Use Huffman coding algorithm
  -d, --decode          Flag to decode specified file
  -p, --performance_eval
                        Runs performance evaluations from /samples folder. Will ignore all other parameters.
```