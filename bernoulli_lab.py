# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:34:38 2018
Recreating the functionality of Matlab code developed in MS thesis project
Takes bitstring, makes dictionary and both encodes and decodes by that
dictionary; also includes functions to help utilize that, including creating 
Bernoulli Sequences
@author: David
"""
import numpy as np

def bern_seq(length,freq):
    """Create a Bernoulli sequence - a random bitstring - of the given length 
    and with the given frequency of 1s"""
    seq = "".join("1" if np.random.rand(1) < freq else "0" for _ in range(length))
    return seq

def dict_words(data_length):
    """Find the maximum possible number of words in a dictionary built from a 
    bitstring of the given length"""
    from numpy import ceil
    max_length = 1.
    sum_lengths = 2.
    total_words = 2.
    while sum_lengths < data_length:
        max_length += 1
        sum_lengths = 2*(max_length*2**max_length - 2**max_length + 1)
    extra_length = sum_lengths - data_length
    total_words = 2**(max_length+1) - 2
    extra_words = ceil(extra_length/max_length)
    final_words = total_words - extra_words
    return int(final_words)

def data_size(dict_size):
    """Find the smallest bitstring length that could generate a dictionary of 
    given size"""
    dict_len = 1
    data_len = 1
    while dict_len < dict_size:
        data_len += 1
        dict_len = dict_words(data_len)
    return data_len

def check_dict(data,dictionary,ii,build_dict = False):
    """Input dataset building dictionary from/encoding by dictionary, current 
    dictionary, current character in dataset, whether we want a longer word 
    than is yet in the dictionary returned"""
    """Start with a length of 1"""
    km = 1
    length = 1
    """Look for the longest word in the dictionary that matches the data"""
    while data[ii:ii+km] in dictionary:
        km += 1
        """If we're adding new words to a dictionary, we want the returned word
        to be longer than the last one that matched, but if we're looking up 
        words in a static dictionary then we want to stick to things in the 
        dictionary"""
        length = km - 1 + int(build_dict)
        """What to do for the string that reaches the end of the data"""
        if build_dict & (ii+length > len(data)):
            return "", km
        elif (not build_dict) & (ii+length == len(data)):
            return data[ii:ii+length],km
    return data[ii:ii+length], length

def bin_words(length, howMany):
    "Creates a sequence of bit strings of a certain length"
    length = int(length)
    howMany = int(howMany)
    for ii in range(howMany):
        yield bin(ii)[2:].zfill(length)

class LZ78Dict(object):
    """Initialize this object by breaking the given data into a dictionary"""
    def __init__(self,data):
        data_length = len(data)
        dict_length_max = dict_words(data_length)
        self.keylength = int(np.ceil(np.log2(dict_length_max)))
        bitno = 0
        self.encode_dict = {}
        for ward in bin_words(self.keylength,dict_length_max):
            buiding = True
            next_w,bitstep = check_dict(data,self.encode_dict,bitno,buiding)
            if next_w == "":
                break
            bitno += bitstep
            self.encode_dict[next_w] = ward
        self.decode_dict = {v: k for k, v in self.encode_iter}
    """Define length as number of entries in the dictionary"""
    def __len__(self):
        return len(self.decode_dict)
    """Give length of the dictionaries as the __repr__ and __str__"""
    def __repr__(self):
        return "Encode & decode dictionaries of ",str(len(self))," entries"
    def __str__(self):
        return repr(self)
    """Turn the encoding dictionary in to an iterable"""
    @property
    def encode_iter(self):
        return self.encode_dict.iteritems()
    """Run strings through the encoding dictionary"""
    def encode(self,message):
        ii = 0
        kryptos = ""
        while ii < len(message):
            not_building = False
            enc_dict = self.encode_dict
            ward,di = check_dict(message,enc_dict,ii,not_building)
            kryptos += self.encode_dict[ward]
            ii += di
        return kryptos
    """Run strings through the decoding dictionary"""
    def decode(self,coded):
        ii = 0
        original = ""
        delta = self.keylength
        while ii < len(coded):
            ward = self.decode_dict[coded[ii:ii+delta]]
            original += ward
            ii += delta
        return original

"""Test the dictWord, BernSeq, __init__, __len__, encode and decode functions & methods"""
if __name__ == "__main__":
    max_key_len = 8
    print "Let's make a dictionary with ",max_key_len,"-bit keys out of a random bitstring"
    dict_len_max = 2**max_key_len
    print "How long should that bitstring be?"
    dat_len = data_size(dict_len_max)
    print "It should be ",dat_len," bits long"
    freq1s = np.random.rand(1)
    print "Let's make it ",round(freq1s*100,1),"% 1's"
    bitstring = bern_seq(dat_len,freq1s)
    print "The first 30 digits are ",bitstring[:30]
    print
    library = LZ78Dict(bitstring)
    dict1 = library.encode_dict
    print "This dictionary has ",len(dict1),"key-value pairs"
    coded1 = library.encode(bitstring)
    print "It was able to encode the bitstring in ",len(coded1)," bits"
    print "The first 30 of those are ",coded1[:30]
    print
    print "Now let's decode that"
    decoded1 = library.decode(coded1)
    print "The first 30 digits of the decoded bitstring are ",decoded1[:30]
    matches = decoded1 == bitstring
    print "It is ",matches," that these code operations are able to reverse each other flawlessly."
