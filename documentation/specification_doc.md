# Project specification

Objective is to use Huffman coding and Lempel-Ziv algorithms to compress losslesly compress files.

## languge
- Project language: English
- For peer-reviews. I am a native finnish speaker

## Problem
Files take up space on hardrive.

## Solution
Make a program that can encode files to smaller size and decode files back to back to original format using Lempel-Ziv and Huffman compression algorithms. 
I chose Lempel-Ziv and Huffman algorithm because they are lossless and no data is lost during compression.

## data strutures

- Huffman coding: binary tree
- *Lempel-Ziv: trie (prefix tree)

or maybe use plain sliding window* 

## Time and space complexity objectives

### Lempel-Ziv
||Time complexity|Space complexity|
|---|---|---|
|encoding|O(n log n)|O(n + m)|
|decoding|O(n)| O(n + m)|

### Huffman
||Time complexity|Space complexity|
|---|---|---|
|encoding|O(n log n)|O(n)|
|decoding|O(n log n)|O(n)|


## sources

- https://en.wikipedia.org/wiki/Huffman_coding
- https://en.wikipedia.org/wiki/LZ77_and_LZ78
- https://www.cs.helsinki.fi/u/tpkarkka/opetus/12k/dct/lecture07.pdf
- https://www.cs.helsinki.fi/u/puglisi/dct2017

## administrative practicalities

I am a bachelor’s in computer science (CS) student.


