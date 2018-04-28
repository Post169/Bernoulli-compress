# Bernoulli-compress
Experiments with compressing random bitstrings
 
bernoulli_lab.py is a Python 2.7.14 module with tools intended for an experiment in compressing random bitstrings (Bernoulli sequences)  
These tools include:  
bern_seq, which creates Bernoulli sequences of any desired length and probability distribution  
dict_words, a function which takes a bitstring length  and returns the greatest LZ78 dictionary size that could be derived from such a bitstring  
data_size, a function which takes a desired maximum dictionary size and uses dict_words to find the length of the shortest bitstring that could produce such a dictionary  
bin_words, a generator that makes a sequence of bitstrings of a given length  
LZ78Dict, an object class that contains a dictionary derived from a string supplied in initialization and has methods to use it to encode and decode other strings  

run_bern_lab.py is a script that calls functionalities from bernoulli_lab.py to compress the elements of the Cartesian product of random bitstrings of nine distributions using LZ78 dictionaries built from random bitstrings of the same nine distributions; the averages of 10 samples of each element are saved in an Excel file  

To see bernoulli_lab.py in action, download it to your computer, open your IDE or other Python console, make sure the working directory in your Python environment is where you saved the file, and either 1) in your IDE click Run or 2) in a console command:  
runfile('[file location of working directory]/bernoulli_lab.py',wdir='[file location of working directory]')
replacing the square brackets with C:/ notation
