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

def snps_to_genotypes(snps):
    return [[snps[i][j] for i in range(len(snps))] for j in range(len(snps[0]))]

def lst_pairhaplotypes(genotypes):
    haplotypes = []
    for genotype in genotypes:
        lst = []
        for snp in genotype:
            if snp == 2:
                # two haplotypes both have alleles 1
                lst.append('1')
            if snp == 1:
                # haplotype 1 can have 1 and haplotype 2 will have 0
                # haplotype 1 can have 0 and haplotype 2 will have 1
                lst.append('x')
            if snp == 0:
                # two haplotypes both have alleles 0
                lst.append('0')
        two_haps = [lst, lst]
        present = False
        for h in haplotypes:
            if h == lst:
                present = True
        if not present:
            haplotypes.append(two_haps)
    return haplotypes


example_genotypes1 = snps_to_genotypes(loadfile("data/example_data_1.txt"))
example_haplotypes1 = lst_pairhaplotypes(example_genotypes1)
