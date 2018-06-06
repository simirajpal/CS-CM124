"""
@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""
import numpy as np
from itertools import chain, groupby

'''
loadfile
	returns an array of lists
	each list is one SNP of the genome
	each entry in the list is one individual
		ex. individual 0 has a genome that is snps[i][0] for all i
'''
def loadfile(file_name):
	data = np.loadtxt(file_name, delimiter = ' ')
	snps = [list(line) for line in data]
	return snps

'''
converts data to list of genotypes
'''
def convert_to_genotypes(snps):
	 return [[snps[i][j] for i in range(len(snps))] for j in range(len(snps[0]))]
	 
'''
lst_haplotypes
	takes in an array of lists representing the genotypes of several individuals
	calls the function possible_haplotypes to determine all of the possible combinations based on
	heterozygous alleles
	return an array of lists representing the possible haplotypes of each individual
'''
def lst_haplotypes(data):
	genotypes = convert_to_genotypes(data)
	unknown_haplotypes = []
	for genotype in genotypes:
		lst = []
		for snp in genotype:
			if snp == 2:
				# two haplotypes both have alleles 1
				lst.append('1')
			if snp == 1:
				# haplotype 1 can have 1 and haplotype 2 will have 0
				# haplotype 1 can have 0 and haplotype 2 will have 1
				lst.append('heterozygous')
			if snp == 0:
				# two haplotypes both have alleles 0
				lst.append('0')
		unknown_haplotypes.append(lst)
	haplotypes = [possible_haplotypes(haplotype) for haplotype in unknown_haplotypes]
	haplotypes = haplotype_pairs(unknown_haplotypes, haplotypes)
	return haplotypes

'''
possible_haplotypes
	takes in a haplotype of some individual genotype where 'heterozygous' is a heterozygous allele
	returns a complete list of possible haplotypes for one individual
'''
  
def possible_haplotypes(haplotype):
	final_haplotype = [[]]
	for snp in haplotype:
		if snp == '0' or snp == '1':
			for pos in final_haplotype:
				pos.append(snp)
		elif snp == 'heterozygous':
			final_haplotype2 = [[] for each in range(len(final_haplotype))]
			for i in range(len(final_haplotype)):
				for j in range(len(final_haplotype[i])):
					final_haplotype2[i].append(final_haplotype[i][j])
			for k in range(len(final_haplotype)):
				final_haplotype[k].append('0')
				final_haplotype2[k].append('1')
			final_haplotype = list(final_haplotype + final_haplotype2)
	return final_haplotype

def haplotype_pairs(unknown_haplotypes, lst_haplotypes):
	haplotype_pairs = []
	for i in range(len(lst_haplotypes)):
		indiv_hap_pairs = []
		for j in range(len(lst_haplotypes[i])):
			haplotype = []
			for k in range(len(lst_haplotypes[i][j])):
				if unknown_haplotypes[i][k] == lst_haplotypes[i][j][k]:
					if lst_haplotypes[i][j][k] == '1':
						haplotype.append('1')
					else:
						haplotype.append('0')
				else:
					if lst_haplotypes[i][j][k] == '1':
						haplotype.append('0')
					else:
						haplotype.append('1')
			pair = [lst_haplotypes[i][j], haplotype]
			rev_pair = [haplotype, lst_haplotypes[i][j]]
			if pair not in indiv_hap_pairs and rev_pair not in indiv_hap_pairs:
				indiv_hap_pairs.append(pair)
		haplotype_pairs.append(indiv_hap_pairs)
	return haplotype_pairs
'''
remove duplicates
	flattens the list of haplotypes and removes all duplicates
	returns a list of all possible haplotypes
'''
def remove_duplicates(possibleHaplotypes):
	possibleHaplotypes = list(chain.from_iterable(possibleHaplotypes))
	possibleHaplotypes.sort()
	result = list(possibleHaplotypes for possibleHaplotypes,_ in groupby(possibleHaplotypes))
	return list(chain.from_iterable(result))
  

# example_haplotypes1 = lst_haplotypes(loadfile("data/example_data_1.txt"))
# print(np.shape(example_haplotypes1))
#haps = lst_haplotypes((loadfile("data/test.txt")))
#print(haps)
#print(remove_duplicates(haps), '\n')
#print(haps)