# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 14:34:38 2018

@author: David
"""
from __future__ import division
import numpy as np

def BernSeq(length,freq):
    seq = ' '*length
    print seq
    for ii in range(length):
        num = np.random.rand(1)
        if num < freq:
            cha = '1'
        else:
            cha = '0'
        seq = seq[:ii] + cha + seq[ii+1:]
    print seq
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
#    print "Length of the data is ", dataLength
#    print "Sum of length of all words is no more than ", sumLengths
#    print "That is ", extraLength, " bits too long"
#    print "That is a total of ", totalWords, " words"
#    print "That's ", extraWords, " more than is needed"
#    print "We need no more than ", finalWords, " words"
    return finalWords

def checkDict(data,webster,ii):
    "Input dataset building dictionary from, dictionary built so far, current"
    km = 1
    while bitz[ii:ii+km] in webster:
        km += 1
        if ii+km > len(bitz):
            return "", km
    return bitz[ii:ii+km], km

def binWords(length, howMany):
    "Creates a sequence of bit strings of a certain length"
    return {}

bitz = BernSeq(20,0.4)
bDL = dictWords(len(bitz))
webster = {}
ii = 0
while ii < bDL:
    print(ii)
    nextW,di = checkDict(bitz,webster,ii)
    ii += di
    webster[nextW] = ii

    
#dl75 = dictWords(75)
#dl76 = dictWords(76)
#dl77 = dictWords(77)
#dl78 = dictWords(78)
#dl79 = dictWords(79)

class LZ78dict(object):
    
    def __init__(self,data):
        datalength = len(data)
        self.dictLengthMax = dictWords(datalength)
        self.keylength = np.ceil(np.log2(self.dictLength))
        bitno = 0
        self.retsbew = {}
        while bitno < datalength:
            nextW,bitstep = checkDict(data,retsbew,bitno)
            bitno += bitstep
            self.retsbew[nextW] = bitno
        self.dictionary = {v: k for k, v in retsbew.iteritems()}