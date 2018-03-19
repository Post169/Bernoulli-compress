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

#bitz = BernSeq(20,0.4)

def dictWords(dataLength):
    from numpy import ceil
#    dataLength = float64(dataLength)
    maxLength = 1.
    sumLengths = 2.
    totalWords = 2.
    print "Length of the data is ", dataLength
    while sumLengths < dataLength:
        maxLength += 1
        sumLengths = 2*(maxLength*2**maxLength - 2**maxLength + 1)
    
    print "Sum of length of all words is no more than ", sumLengths
    extraLength = sumLengths - dataLength
    print "That is ", extraLength, " bits too long"
    totalWords = 2**(maxLength+1) - 2
    print "That is a total of ", totalWords, " words"
    extraWords = ceil(extraLength/maxLength)
    print "That's ", extraWords, " more than is needed"
    finalWords = totalWords - extraWords
    print "We need no more than ", finalWords, " words"
    return finalWords

dl75 = dictWords(75)
#dl76 = dictWords(76)
#dl77 = dictWords(77)
#dl78 = dictWords(78)
#dl79 = dictWords(79)

class LZ78dict(object):
    
    def __init__(self,data):
        datalength = len(data)
        self.dictLength = dictWords(datalength)
        self.keylength = np.ceil(np.log2(self.dictLength))
        