# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:13:19 2018
Adapted from Bhrigu Srivastava's code shown on
http://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
Bhrigu's code took filename of .txt and returned filename of created .bin, and 
vice versa; this takes string and list of words and returns string.
@author: David
"""

import heapq

class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	def __cmp__(self, other):
		if(other == None):
			return -1
		if(not isinstance(other, HeapNode)):
			return -1
		return self.freq > other.freq


class HuffmanCoding:
    def __init__(self, data, words):#DCN
        self.data = data
        self.words = words
        self.codes = {}
        self.reverse_mapping = {}
        self.freq_dict = self.make_frequency_dict()
        self.heap = self.make_heap()
        self.compressed = self.compress(self.data)

	""" functions for compression:"""
    def make_frequency_dict(self):#DCN
        frequency = {}
        for phrase in self.words:
            if not phrase in frequency:
                frequency[phrase] = 0
            frequency[phrase] += 1
        return frequency
    
    def make_heap(self):#DCN
        frequency = self.freq_dict
        heap = []
        for key in frequency:
            node = HeapNode(key, frequency[key])
            heapq.heappush(heap, node)
        return heap

    def merge_nodes(self):#DCN
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            
            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):#DCN
        if(root == None):
            return
        
        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):#DCN
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
    
    def compress(self,text):
        self.merge_nodes()
        self.make_codes()
        encoded_text = ""
        for phrase in text:
            encoded_text += self.codes[phrase]
        
        print("Compressed")
        return encoded_text #output_path

	""" functions for decompression: """
    
    def decompress(self, encoded_text):#previously decode_text
        current_code = ""
        decoded_text = ""
        
        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        
        return decoded_text

