|file name                             |algorithm |encode time (s)|decode time (s)|size (KB)|compressed size(KB)|space saved (%)|
|--------------------------------------|----------|---------------|---------------|---------|-------------------|---------------|
|munkki_kammio.txt                     |Huffman   |0.009027       |0.05303        |84175    |48343              |42.568%        |
|munkki_kammio.txt                     |lempel-ziv|1.508167       |0.055931       |84175    |42683              |49.293%        |
|The_Count_of_Monte_Cristo_by_Dumas.txt|Huffman   |0.293797       |1.932397       |2786944  |1642615            |41.06%         |
|The_Count_of_Monte_Cristo_by_Dumas.txt|lempel-ziv|2149.073724    |1.913253       |2786944  |1435244            |48.501%        |
|test.txt                              |Huffman   |0.000389       |6.7e-05        |49       |18                 |63.265%        |
|test.txt                              |lempel-ziv|0.000548       |7.7e-05        |49       |12                 |75.51%         |
|100_input.txt                         |Huffman   |0.000254       |0.000187       |100      |150                |-50.0%         |
|100_input.txt                         |lempel-ziv|0.000778       |9.5e-05        |100      |113                |-13.0%         |
|100000_input.txt                      |Huffman   |0.012321       |0.091635       |100000   |83972              |16.028%        |
|100000_input.txt                      |lempel-ziv|0.960896       |0.084459       |100000   |109133             |-9.133%        |
|1000000_input.txt                     |Huffman   |0.120917       |0.964004       |1000000  |839698             |16.03%         |
|1000000_input.txt                     |lempel-ziv|25.396861      |0.831118       |1000000  |1090813            |-9.081%        |