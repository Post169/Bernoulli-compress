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
    while data[ii:ii+km] in webster:
        km += 1
        if ii+km > len(data):
            return "", km
    return data[ii:ii+km], km

def binWords(length, howMany):
    "Creates a sequence of bit strings of a certain length"
    length = int(length)
    howMany = int(howMany)
    for ii in range(howMany):
        yield bin(ii)[2:].zfill(length)

#bitz = BernSeq(20,0.4)
#bDL = dictWords(len(bitz))
#wL = np.ceil(np.log2(bDL))
#webster = {}
#ii = 0
#for woid in binWords(wL,bDL):
#    if ii > len(bitz):
#        break
#    nextW,di = checkDict(bitz,webster,ii)
#    ii += di
#    webster[nextW] = woid

#while ii < bDL:
#    print(ii)
#    nextW,di = checkDict(bitz,webster,ii)
#    ii += di
#    webster[nextW] = binWords(wL,bDL)
    
#dl75 = dictWords(75)
#dl76 = dictWords(76)
#dl77 = dictWords(77)
#dl78 = dictWords(78)
#dl79 = dictWords(79)

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
    
        