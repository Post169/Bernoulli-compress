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

def BernSeq(length,freq):
    """Create a Bernoulli sequence - a random bitstring - of the given length 
    and with the given frequency of 1s"""
    seq = "".join("1" if np.random.rand(1) < freq else "0" for _ in range(length))
    return seq

def dictWords(dataLength):
    """Find the maximum possible number of words in a dictionary built from a 
    bitstring of the given length"""
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

def dataSize(dictSize):
    """Find the smallest bitstring length that could generate a dictionary of 
    given size"""
    dictlen = 1
    datalen = 1
    while dictlen < dictSize:
        datalen += 1
        dictlen = dictWords(datalen)
    return datalen

def checkDict(data,dictionary,ii,buildDict = False):
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
        length = km - 1 + int(buildDict)
        """What to do for the string that reaches the end of the data"""
        if buildDict & (ii+length > len(data)):
            return "", km
        elif (not buildDict) & (ii+length == len(data)):
            return data[ii:ii+length],km
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
        return "Encode & decode dictionaries of ",str(len(self))," entries"
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
            notBuilding = False
            encDict = self.encodeDict
            ward,di = checkDict(message,encDict,ii,notBuilding)
            kryptos += self.encodeDict[ward]
            ii += di
        return kryptos
    """Run strings through the decoding dictionary"""
    def decode(self,coded):
        ii = 0
        original = ""
        delta = self.keylength
        while ii < len(coded):
            ward = self.decodeDict[coded[ii:ii+delta]]
            original += ward
            ii += delta
        return original

"""Test the dictWord, BernSeq, __init__, __len__, encode and decode functions & methods"""
def demonstrate():
    maxKeyLen = 8
    print "Let's make a dictionary with ",maxKeyLen,"-bit keys out of a random bitstring"
    dictLenMax = 2**maxKeyLen
    print "How long should that bitstring be?"
    datlen = dataSize(dictLenMax)
    print "It should be ",datlen," bits long"
    omega = np.random.rand(1)
    print "Let's make it ",round(omega*100,1),"% 1's"
    bitstring = BernSeq(datlen,omega)
    print "The first 30 digits are ",bitstring[:30]
    library = LZ78dict(bitstring)
    dict1 = library.encodeDict
    print "This dictionary has ",len(dict1),"key-value pairs"
    coded1 = library.encode(bitstring)
    print "It was able to compress the bitstring to ",len(coded1)," bits"
    print "The first 30 of those are ",coded1[:30]
    print "Now let's decode that"
    decoded1 = library.decode(coded1)
    print "The first 30 digits of the decoded bitstring are ",decoded1[:30]
    matches = decoded1 == bitstring
    print "It is ",matches," that these code operations are able to reverse each other flawlessly."
