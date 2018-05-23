# -*- coding: utf-8 -*-
"""
Created on Tue May 22 21:11:51 2018

@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""
import numpy as np

'''
loadfile
    returns an array of lists
    each list is one SNP of the genome
    each entry in the list is one individual
        ex. individual 0 has a genome that is snps[i][0] for all i
'''
def loadfile(file_name):
    data = np.loadtxt(file_name, delimiter = ' ')
    snps = []
    for line in data:
        snps.append(list(line))
    snps = np.array(snps)
    return snps


example_data1 = loadfile("data/example_data_1.txt")
