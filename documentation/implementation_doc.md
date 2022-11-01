# Implementation document

## Lempel-Ziv

Data is encoded in 2 different kind of blocks.

|  1 bit header |                            |          |
|---:           |---                         |---       |
|  header       | 1 byte of data             |          |
|  1            | 1 0 1 0 1 0 1 0            |          |
|               |                            |          |
|  0            | 1 0 1 0 1 0 1 0 1 0 1 0    | 1 1 1 1  |
|  header       | 12bits relative distance   | length 4 bits  |

Both data blocks have 1 bit header to differentiate between them.

If there is no prior data to reference program saves 1 bit header and 8 bits of the original data.

If within the last 4095 bytes there is a 2 - 15 byte sequence that can be referenced then we use 1 bit header 12 bit for distance for matching region and 4 bits for the length of the region.

If the length of the encoded data bit is not divisible by 8, then the last byte is filled zero bits.

### Time complexity

#### Encoding
|                                           |            |
|---                                        |--          |
|Suffix array                               |O(n log n ) |
|Longest common prefix array                | O(n)       |
|binary search matching suffix array regions| O(log n)   |

Because binary search over suffix array is performed for every byte. 

Overall complexity is **O(n log n)**

#### Decoding 

Single loop over the encoded file.
**O(n)**

## Huffman coding

Format of encoded file
|          |     |
| ---      | --- |
|  3 bits  | amount of bits empty bits at end 0-7    |
|  n bits  | huffman tree, 0 for non-leaf node, 1 for leaf node |
|       | after 1 there is one byte of data representing node content |
| n bits| data encoded with huffman codes|
| 0-7 bits| empty bits to get bitwise length to be divisible by 8 |

### Time complexity

#### Encoding
Input data is iterated byte by byte and frequencies saved to a dictionary.
Dictionary is sorted and huffman tree generated from it.
Input data is iterated again and every byte is saved to output array by the representing Huffman code.

**O(n)**


#### Decoding
Huffman tree is generated according to header. Iterate through file and and save bytes represented by huffmancodes to outputbuffer

**O(n)**


## Performance results

|file name                             |algorithm |encode time (s)|decode time (s)|size (KB)|compressed size(KB)|space saved (%)|
|--------------------------------------|----------|---------------|---------------|---------|-------------------|---------------|
|munkki_kammio.txt                     |Huffman   |0.009676       |0.056108       |84175    |48343              |42.568%        |
|munkki_kammio.txt                     |lempel-ziv|0.828812       |0.059813       |84175    |42698              |49.275%        |
|The_Count_of_Monte_Cristo_by_Dumas.txt|Huffman   |0.323205       |1.968108       |2786944  |1642615            |41.06%         |
|The_Count_of_Monte_Cristo_by_Dumas.txt|lempel-ziv|28.63678       |2.224113       |2786944  |1435368            |48.497%        |
|test.txt                              |Huffman   |0.000156       |7.5e-05        |49       |18                 |63.265%        |
|test.txt                              |lempel-ziv|0.000629       |9.3e-05        |49       |14                 |71.429%        |
|100_input.txt                         |Huffman   |0.000325       |0.000224       |100      |155                |-55.0%         |
|100_input.txt                         |lempel-ziv|0.001109       |9.9e-05        |100      |113                |-13.0%         |
|100000_input.txt                      |Huffman   |0.015419       |0.104418       |100000   |83970              |16.03%         |
|100000_input.txt                      |lempel-ziv|1.029243       |0.094574       |100000   |109113             |-9.113%        |
|1000000_input.txt                     |Huffman   |0.147546       |1.082887       |1000000  |839612             |16.039%        |
|1000000_input.txt                     |lempel-ziv|10.436223      |0.943553       |1000000  |1091023            |-9.102%        |
