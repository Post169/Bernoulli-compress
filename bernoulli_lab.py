# -*- coding: UTF-8 -*-
"""
Created on Wed Feb 21 14:34:38 2018
Takes bitstring, makes dictionary and both encodes and decodes by that
dictionary; also includes functions to help utilize that, including 
creating Bernoulli Sequences
Run to see demonstration
@author: David
"""

from __future__ import print_function
import numpy as np

def bern_seq(length, freq1s):
    """bern_seq creates Bernoulli sequence (random bitstring) of given
    length with given freq of 1s
    """
    return tuple(int(np.random.rand(1) < freq1s) for _ in range(length))


def dict_words(data_length):
    """dict_words finds max possible number of words in a dictionary
    built by LZ78 algorithm from a bitstring of given length
    """
    max_length = 1
    sum_lengths = 2
    total_words = 2
    while sum_lengths < data_length:
        max_length += 1
        sum_lengths = 2*(max_length*2**max_length - 2**max_length + 1)
    extra_length = sum_lengths - data_length
    total_words = 2*(2**max_length - 1)
    extra_words = (extra_length + max_length - 1)//max_length
    return total_words - extra_words


def data_size(dict_size):
    """data_size finds min bitstring length that could generate
    dictionary of given size; inverse function of dict_words
    """
    dict_len = 1
    data_len = 1
    while dict_len < dict_size:
        data_len += 1
        dict_len = dict_words(data_len)
    return data_len


def bin_words(length, howMany):
    """bin_words generates a sequence of bit strings of specified length"""
    length = int(length)
    howMany = int(howMany)
    for ii in xrange(howMany):
        bin_string = bin(ii)[2:].zfill(length)
        yield tuple([int(x) for x in bin_string])


class LZ78Dict(object):
    
    def __init__(self, data):
        """Create LZ78Dict object by breaking the given data into a
        dictionary
        """
        self._data30 = data[:30]
        dict_length_max = dict_words(len(data))
        self.keylength = int(np.ceil(np.log2(dict_length_max)))
        bitno = 0
        self.encode_dict = {}
        #Create a Lempel-Ziv '78 dictionary mapping equal-length code
        #words with words of increasing length that concatenate to
        #make the original data:
        for ward in bin_words(self.keylength, dict_length_max):
            building = True
            next_w,bitstep = self._check_dict(data, self.encode_dict, bitno, building)
            if next_w == "":
                break
            bitno += bitstep
            self.encode_dict[next_w] = ward
        #Turn the dictionary just created into its reverse, to decode:
        self.decode_dict = {v: k for k, v in self.encode_iter}
    
    def __len__(self):
        """Define __len__ as number of entries in the dictionary"""
        return len(self.decode_dict)
    
    def __repr__(self):
        """How to create current instance again as __repr__"""
        return "LZ78Dict(({self._data30[:]}...))".format(self=self)
    
    def __str__(self):
        """Give length of the dictionaries as the __str__"""
        return "Encode & decode dictionaries of " + str(len(self)) + " entries each"
    
    @property
    def encode_iter(self):
        """Turn the encoding dictionary into encode_iter iterable 
        property
        """
        return self.encode_dict.iteritems()
    
    def encode(self, message):
        """encode method expresses given tuple in terms of encode 
        dictionary
        """
        ii = 0
        kryptos = ()
        while ii < len(message):
            not_building = False
            enc_dict = self.encode_dict
            ward,di = self._check_dict(message, enc_dict, ii, not_building)
            kryptos += self.encode_dict[ward]
            ii += di
        return kryptos
    
    def decode(self, coded):
        """decode method expresses given tuple in terms of decode 
        dictionary
        """
        ii = 0
        original = ()
        delta = self.keylength
        while ii < len(coded):
            ward = self.decode_dict[coded[ii:ii+delta]]
            original += ward
            ii += delta
        return original
    
    @staticmethod
    def _check_dict(data, dictionary, ii, build_dict=False):
        """check_dict searches given data tuple, starting at position
        ii, for largest matching sequence in given dictionary; if 
        build_dict, goes one element farther
        """
        #km is length of tuple to be compared to dictionary; length is
        #tuple elements checked for reaching or exceeding data length
        #(default reaching; exceeding if build_dict)
        km = 1
        length = 1
        #Look for the longest sequence in the dictionary that matches
        #the data, from where we're starting as far on as possible
        while data[ii:ii+km] in dictionary:
            km += 1
            length = km - 1 + int(build_dict)
            #When the sequence we're building reaches or passes the
            #end of the data, what to do depends on whether we are
            #building a new dictionary or reading from one:
            if build_dict & (ii+length > len(data)):
                return "", km
            elif (not build_dict) & (ii+length == len(data)):
                return data[ii:ii+length], km
        return data[ii:ii+length], length


"""Run module as command to see demonstration of functionalities"""
if __name__ == "__main__":
    max_key_len = 8
    dict_len_max = 2**max_key_len
    dat_len = data_size(dict_len_max)
    
    print("Let's make a dictionary with ", max_key_len, 
           "-bit keys out of a random bitstring")
    print("How long should that bitstring be if we want max length but")
    print(" certainty of 8-bit keys?")
    print("It should be ", dat_len, " bits long")
    
    freq1s = np.random.rand(1)
    bitstring = bern_seq(dat_len, freq1s)
    
    print("Let's make it ", round(freq1s*100,1), "percent 1's")
    print("The first 30 digits are ", bitstring[:30])
    print()
    
    library = LZ78Dict(bitstring)
    dict1 = library.encode_dict
    coded1 = library.encode(bitstring)
    
    print("This dictionary has ", len(dict1), "key-value pairs")
    print("It was able to encode the bitstring in ", len(coded1), " bits")
    print("The first 30 of those are ", coded1[:30])
    print()
    print("Now let's decode that")
    
    decoded1 = library.decode(coded1)
    matches = decoded1 == bitstring
    
    print("The first 30 digits of the decoded bitstring are ", decoded1[:30])
    print("It is ", matches, " that these code operations are able to",
           "reverse each other flawlessly.")