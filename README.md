# Bernoulli-compress
Experiments with compressing random bitstrings
 
bernoulli_lab.py is a Python 2.7.14 module with tools intended for an experiment in compressing random bitstrings (Bernoulli sequences)  
These tools include:

`bern_seq`, which creates Bernoulli sequences of any desired length and probability distribution
> Example 1: `bern_seq(200,.87)` will create a 200-tuple of zeros and ones, with about 134 (87%) of those being 1s  
> Example 2: `bern_seq(20,.2)` might return `(1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1)`

dict_words, a function which takes a bitstring length and returns the greatest LZ78 dictionary size that could be derived from such a bitstring  
> Example: `dict_words(1024)` will return `180`; a dictionary built by the LZ78 algorithm from sequence of 1024 bits will never have more than 180 "words" in it

`data_size`, a function which takes a desired maximum dictionary size and uses dict_words to find the length of the shortest bitstring that could produce such a dictionary  
> Example: `data_size(180)` will return `1020`; the smallest bitstring that could be turned into a dictionary of 180 words by the LZ78 algorithm is 1020 bits long

`bin_words`, a generator that makes a sequence of bitstrings of a given length  
> Example: `bin_words(5,25)` will create a generator that will put out a sequence of five-bit bitstrings, starting with `(0,0,0,0,0)` and incrementing in binary style each time it is called until it has reached the 25th, when it will tell the looping mechanism that it has reached the end of the sequence

`LZ78Dict`, an object class that contains a dictionary derived from a string supplied in initialization and has methods to use it to encode and decode other strings  
> Example: `webster = LZ78Dict(bern_seq(1020,.5))` will create an object containing dictionaries of equal size, with up to 180 words each. One is referred to as `webster.encode_dict`, to be used for compressing bitstrings that contain similar numbers of 1s and 0s, and the other referred to as `webster.decode_dict`, to be used for decompressing those compressed bitstrings. `webster.encode_dict` can be used to compress bitstring `bin_data = bern_seq(160,.6)` very easily, without directly referring to it, by calling `compressed_data = webster.encode(bin_data)`. Likewise, you can recover `bin_data` by calling `bin_data_back = webster.decode(compressed_data)`

run_bern_lab.py is a script that calls functionalities from bernoulli_lab.py to compress the elements of the Cartesian product of random bitstrings of nine distributions using LZ78 dictionaries built from random bitstrings of the same nine distributions; the averages of 10 samples of each element are saved in an Excel file

To see bernoulli_lab.py in action, download it to your computer, open your IDE or other Python console, make sure the working directory in your Python environment is where you saved the file, and either 1) in your IDE click Run or 2) in a console command:  
runfile('[file location of working directory]/bernoulli_lab.py',wdir='[file location of working directory]')
replacing the square brackets with C:/ notation
