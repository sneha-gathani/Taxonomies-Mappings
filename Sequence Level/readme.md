# Code

1. regexFormat.py script is used by the sequence.py file to get all interaction embeddings in a single concatenated non-space string. It also has functions to calculate the count of number of sequences observed for interaction log datasets using the regular expressions found and shared in the sequence embeddings.
2. sequence.py provides the count of all sequences of the three sequence level taxonomies in the three interaction log datasets. To run the code -
```
python sequence.py
```
An example of number of Gotz and Wen sequences found for the Wall interaction log dataset using Brehmer and Munzner interaction level taxonomy as the underlying interaction level taxonomy is:
```
Gotz and Wen via Brehmer and Munzner taxonomy: {'scan': 579, 'flip': 337, 'swap': 124, 'drill-down': 699}
```
Here, we see 579 _scan_, 337 _flip_, 124 _swap_ and 699 _drill-down_ sequences of the Gotz and Wen taxonomy in the Wall interaction log dataset.
