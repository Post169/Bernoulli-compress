# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:34:38 2018

@author: David
"""
# from __future__ import division
import numpy as np

def BernSeq(length,freq):
    """Create a Bernoulli sequence - a random bitstring - of the given length and given frequency of 1s"""
    seq = ' '*length
    #print seq
    for ii in range(length):
        num = np.random.rand(1)
        if num < freq:
            cha = '1'
        else:
            cha = '0'
        seq = seq[:ii] + cha + seq[ii+1:]
    #print seq
    return seq

def dictWords(dataLength):
    """Find the maximum possible number of words in a dictionary built from a bitstring of the given length"""
    from numpy import ceil
    maxLength = 1.
    sumLengths = 2.
    totalWords = 2.
    while sumLengths < dataLength:
        maxLength += 1
        sumLengths = 2*(maxLength*2**maxLength - 2**maxLength + 1)
    extraLength = sumLengths - dataLength
    totalWords = 2**(maxLength+1) - 2
    extraWords = ceil(extraLength/maxLength)
    finalWords = totalWords - extraWords
    return int(finalWords)

def checkDict(data,dictionary,ii,buildDict = False):
    """Input dataset building dictionary from/encoding by dictionary, current dictionary, current character in
    dataset, whether we want a longer word than is yet in the dictionary returned"""
    """Start with a length of 1"""
    km = 1
    length = 1
    """Look for the longest word in the dictionary that matches the data"""
    while data[ii:ii+km] in dictionary:
        km += 1
        """If we're adding new words to a dictionary, we want the final word to be longer than the last one that
        matched, but if we're finding words in a dictionary then we want to stick to things in the dictionary"""
        length = km - 1 + int(buildDict)
        """What to do for the string that reaches the end of the data"""
        if buildDict & (ii+length > len(data)):
            return "", km
        elif (not buildDict) & (ii+length == len(data)): #& (data[ii:ii+length] in dictionary):
            return data[ii:ii+length],km
        # if km > 10:
        #     print "km = ",km ,", ii = ",ii,", len(dict) = ",len(webster)," building = ",buildDict
        #     print cut & ii+km > len(data)
    return data[ii:ii+length], length

def binWords(length, howMany):
    "Creates a sequence of bit strings of a certain length"
    length = int(length)
    howMany = int(howMany)
    for ii in range(howMany):
        yield bin(ii)[2:].zfill(length)

class LZ78dict(object):
    """Initialize this object by breaking the given data into a dictionary"""
    def __init__(self,data):
        datalength = len(data)
        self.dictLengthMax = dictWords(datalength)
        self.keylength = int(np.ceil(np.log2(self.dictLengthMax)))
        bitno = 0
        self.encodeDict = {}
        for ward in binWords(self.keylength,self.dictLengthMax):
            buiding = True
            nextW,bitstep = checkDict(data,self.encodeDict,bitno,buiding)
            if nextW == "":
                break
            bitno += bitstep
            self.encodeDict[nextW] = ward
        self.decodeDict = {v: k for k, v in self.encodeIter}
    """Define length as number of entries in the dictionary"""
    def __len__(self):
        return len(self.decodeDict)
    """Give length of the dictionaries as the __repr__ and __str__"""
    def __repr__(self):
        return "Encode & decode dictionaries of ",len(self)," entries"
    def __str__(self):
        return repr(self)
    """Turn the encoding dictionary in to an iterable"""
    @property
    def encodeIter(self):
        return self.encodeDict.iteritems()
    """Run strings through the encoding dictionary"""
    def encode(self,message):
        ii = 0
        kryptos = ""
        while ii < len(message):
            building = False
            ward,di = checkDict(message,self.encodeDict,ii,building)
            kryptos += self.encodeDict[ward]
            ii += di
#            print ward
            if ii > (len(message) - 10):
                print 'getting close'
        return kryptos
    """Run strings through the decoding dictionary"""
    def decode(self,coded):
        ii = 0
        original = ""
        delta = self.keylength
        while ii < len(coded):
            ward = self.decodeDict[coded[ii:ii+delta]]
            original += ward
            print ii,' ',ward
            ii += delta
        return original


"""Test the dictWord, BernSeq, __init__, __len__, and encode functions & methods"""
dlen128cww = 0 # put datalength needed to require 128 code words here
dictlen = 0 # keep track of the dictionary length here
while dictlen < 128:
    dlen128cww += 1
    dictlen = dictWords(dlen128cww)
print "To get 128 words in dict, data will be ",dlen128cww," bits long"
sample60 = BernSeq(dlen128cww,.6) # Bernoulli sequence to make a 128 word dict
print "The Bernoulli sequence is ",len(sample60)," bits long"
webster = LZ78dict(sample60)
print "The dictionary has ",len(webster)," words"
coded_sample60 = webster.encode(sample60)
print "The encoded form of the data is ",coded_sample60
decoded_sample60 = webster.decode(coded_sample60)
print "It is ",decoded_sample60==sample60," that the encode and decode methods both work"