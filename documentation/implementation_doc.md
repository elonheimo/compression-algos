
|file name                             |algorithm |encode time (s)|decode time (s)|size (KB)|compressed size(KB)|space saved (%)    |
|--------------------------------------|----------|---------------|---------------|---------|-------------------|-------------------|
|munkki_kammio.txt                     |Huffman   |0.010273       |0.055088       |84175    |48343              |42.568%            |
|munkki_kammio.txt                     |lempel-ziv|1.128707       |0.025913       |84175    |94697              |-12.5%             |
|The_Count_of_Monte_Cristo_by_Dumas.txt|Huffman   |0.308081       |1.833561       |2786944  |1642615            |41.06%             |
|The_Count_of_Monte_Cristo_by_Dumas.txt|lempel-ziv|47.381454      |0.797769       |2786944  |3135312            |-12.5%             |
|test.txt                              |Huffman   |0.000155       |7.9e-05        |49       |18                 |63.265%            |
|test.txt                              |lempel-ziv|0.000412       |6.5e-05        |49       |56                 |-14.286%           |
|100_input.txt                         |Huffman   |0.000304       |0.000221       |100      |161                |-61.0%             |
|100_input.txt                         |lempel-ziv|0.000702       |8.2e-05        |100      |113                |-13.0%             |
|100000_input.txt                      |Huffman   |0.013175       |0.095272       |100000   |83993              |16.007%            |
|100000_input.txt                      |lempel-ziv|1.296583       |0.029622       |100000   |112500             |-12.5%             |
|1000000_input.txt                     |Huffman   |0.12826        |0.885247       |1000000  |839647             |16.035%            |
|1000000_input.txt                     |lempel-ziv|15.21236       |0.287221       |1000000  |1125000            |-12.5%             |

