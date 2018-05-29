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
    genotypes = []
    for line in data:
        genotypes.append(list(line))
    genotypes = np.array(genotypes)
    return genotypes

'''
lst_haplotypes
    takes in an array of lists representing the genotypes of several individuals
    return an array of lists representing the haplotypes corresponding
        these haplotypes contain an x for heterozygous alleles
'''
def lst_haplotypes(genotypes):
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
        present = False
        for h in haplotypes:
            if h == lst:
                present = True
        if not present:
            haplotypes.append(lst)
    return haplotypes

'''
possible_haplotypes
    takes in a list of haplotypes for individuals where x is a heterozygous allele
    returns a complete list of possible haplotypes
        every time an x is encountered, it adds another possible haplotype with the 1 allele representing
        the heterozygous allele rather than the 0 allele
'''
def possible_haplotypes(haplotypes):
    final_haplotypes = []
    for haplotype in haplotypes:
        final_haplotype = []
        for snp in haplotype:
            if snp == '0' or snp == '1':
                final_haplotype.append(snp)
            elif snp == 'x':
                final_haplotype2 = []
                for allele in final_haplotype:
                    final_haplotype2.append(allele)
                final_haplotype.append('0')
                final_haplotype2.append('1')
        if len(final_haplotype2) == len(final_haplotype):
            final_haplotypes.append(final_haplotype2)
        final_haplotypes.append(final_haplotype)      
    return final_haplotypes
                
# example_haplotypes1 = lst_haplotypes(loadfile("data/example_data_1.txt"))
# example_possible_haplotypes1=possible_haplotypes(example_haplotypes1)
# print(np.shape(example_possible_haplotypes1))
test = possible_haplotypes(lst_haplotypes((loadfile("data/test.txt"))))
print(test)