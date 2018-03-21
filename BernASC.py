# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:34:38 2018

@author: David
"""
from __future__ import division
import numpy as np

def BernSeq(length,freq):
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
    return finalWords

def checkDict(data,webster,ii,cut=True):
    "Input dataset building dictionary from, dictionary built so far, current"
    km = 1
    while data[ii:ii+km] in webster:
        km += 1
        if km%5 == 0:
            print km
        if cut & ii+km > len(data):
            return "", km
    return data[ii:ii+km], km

def binWords(length, howMany):
    "Creates a sequence of bit strings of a certain length"
    length = int(length)
    howMany = int(howMany)
    for ii in range(howMany):
        yield bin(ii)[2:].zfill(length)

class LZ78dict(object):
    
    def __init__(self,data):
        datalength = len(data)
        self.dictLengthMax = dictWords(datalength)
        self.keylength = np.ceil(np.log2(self.dictLengthMax))
        bitno = 0
        self.encodeDict = {}
        for ward in binWords(self.keylength,self.dictLengthMax):
            nextW,bitstep = checkDict(data,self.encodeDict,bitno)
            if nextW == "":
                break
            bitno += bitstep
            self.encodeDict[nextW] = ward
        self.decodeDict = {v: k for k, v in self.encodeDict.iteritems()}
    def __len__(self):
        return len(self.decodeDict)
    def __repr__(self):
        return "Encode dictionary: ",self.encodeDict,"Decode dictionary: ",\
    self.decodeDict
    def __str__(self):
        return repr(self)
    def encode(self,message):
        ii = 0
        kryptos = ""
        while ii < len(message):
            ward,di = checkDict(message,self.encodeDict,ii,False)
            kryptos += ward
        return kryptos
    def decode(self,coded):
        ii = 0
        original = ""
        while ii < len(coded):
            ward,di = checkDict(coded,self.decodeDict,ii,False)
            original += ward
        return original

dlen128cww = 0 # put datalength needed to require 128 code words here
dictlen = 0 # keep track of the dictionary length here
while dictlen < 128:
    dlen128cww += 1
    dictlen = dictWords(dlen128cww)
print dlen128cww
sample60 = BernSeq(dlen128cww,.6) # Bernoulli sequence to make a 128 word dict
print len(sample60)
webster = LZ78dict(sample60)
print len(webster)
coded_sample60 = webster.encode(sample60)
print coded_sample60