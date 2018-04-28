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

Dists = (2**-5,2**-4,2**-3,2**-2,2**-1,1-2**-2,1-2**-3,1-2**-4,1-2**-5)
Width = len(Dists)
Heatmap = np.zeros((Width,Width))

for IdxDict,ValDict in enumerate(Dists):
    DictSeed = bl.bern_seq(65536,ValDict)
    Webster = bl.LZ78Dict(DictSeed)
    for IdxShade,ValShade in enumerate(Dists):
        Compr = []
        for Label in range(10):
            Message = bl.bern_seq(512,ValShade)
            Kryptos = Webster.encode(Message)
            Score = len(Kryptos)
            Compr += [Score]
        Heatmap[IdxShade,IdxDict] = np.mean(Compr)

for Spot in it.product(range(Width), repeat=2):
    worksheet.write(Spot[0],Spot[1],Heatmap[Spot])

workbook.close()