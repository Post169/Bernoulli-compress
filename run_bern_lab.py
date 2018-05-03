# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 09:28:33 2018
Create random bitstrings of various probability distributions, create code
dictionaries from them, use those to encode more bitstrings, and record the
average compressed length of each combination of probability distributions on
an Excel sheet
@author: David
"""

import bernoulli_lab as bl
import numpy as np
import xlsxwriter as xl
import itertools as it

workbook = xl.Workbook('Python heatmaps.xlsx')
worksheet = workbook.add_worksheet()

dists = (2**-5,2**-4,2**-3,2**-2,2**-1,1-2**-2,1-2**-3,1-2**-4,1-2**-5)
width = len(dists)
heatmap = np.zeros((width,width))

for idx_dict,val_dict in enumerate(dists):
    dict_seed = bl.bern_seq(65536,val_dict)
    webster = bl.LZ78Dict(dict_seed)
    for idx_shade,val_shade in enumerate(dists):
        compr = []
        for label in range(10):
            message = bl.bern_seq(512,val_shade)
            kryptos = webster.encode(message)
            score = len(kryptos)
            compr += [score]
        heatmap[idx_shade,idx_dict] = np.mean(compr)

for spot in it.product(range(width), repeat=2):
    worksheet.write(spot[0],spot[1],heatmap[spot])

workbook.close()