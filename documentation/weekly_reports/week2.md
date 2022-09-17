Tried to implement lempel ziv algorithm with suffix arrays.
It's somewhat working but for some reason decompressing with bigger files is  currently an issue. Also I am a bit uncertain about the time efficiency of my current algorithm.

Idea:

1 bit flag for 1 byte if no match

0|00000000

1 bit flag, 12 bits for relative distance to compressing index, 4bits for match length

1|000000000000|0000

12 bits for storing relative distance so i could refer up 4095 bytes back when compressing 

Hopefully next week will be more productive for the project. Did not commit any code to github because it's full of obscure print statements and comments.  

Time spent: 15 hours