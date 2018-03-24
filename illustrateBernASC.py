# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 17:31:22 2018
Illustrate the operations of BernASC.py
@author: David
"""
import BernASC as BA
import numpy as np

maxKeyLen = 8
print "Let's make a dictionary with ",maxKeyLen,"-bit keys out of a random bitstring"
dictLenMax = 2^maxKeyLen
print "How long should that bitstring be?"
datlen = BA.dataSize(dictLenMax)
print "It should be ",datlen," bits long"
omega = np.random.rand(1)
print "Let's make it ",round(omega*100,1),"% 1's"
bitstring = BA.BernSeq(datlen,omega)
print "The first 30 digits are ",bitstring[:30]
dict1 = BA.LZ78dict(bitstring)
print "This dictionary has ",len(dict1),"key-value pairs"
coded1 = dict1.encode(dict1)
print "It was able to compress the bitstring to ",len(coded1)," bits"
print "The first 30 of those are ",coded1[:30]
print "Now let's decode that"
decoded1 = dict1.decode(coded1)
print "The first 30 digits of the decoded bitstring are ",decoded1
matches = decoded1 == bitstring
print "It is ",matches," that these code operations are able to reverse each other flawlessly."