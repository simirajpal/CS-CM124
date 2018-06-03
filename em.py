"""
@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""

import phasing
import numpy as np
from itertools import chain

# freq_lst needs to be a dictionary
def expectation_step(haplotypes, hap_pairs, freq_lst):
	probabilities = []
	for i in range(len(hap_pairs)):
		probability = []
		for p in range(len(hap_pairs[i])):
			f1 = freq_lst[''.join(hap_pairs[i][p][0])]
			f2 = freq_lst[''.join(hap_pairs[i][p][1])]
			probability.append(find_probability(f1, f2, len(hap_pairs[i])))
		probabilities.append(probability)
	frequencies = {}	
	for haplotype in haplotypes:
		probs = []
		for j in range(len(hap_pairs)):
			for q in range(len(hap_pairs[j])):
				if hap_pairs[j][q][0] == haplotype or hap_pairs[j][q][1] == haplotype:
					probs.append(probabilities[j][q])
		frequencies[''.join(haplotype)] = find_frequency(probs, len(haplotypes))
	return frequencies, probabilities			

def find_probability(freq1, freq2, numOfPairs):
	return (freq1*freq2)/(numOfPairs*freq1*freq2)
	
def find_frequency(probs, numOfPossibleHaps):
	return sum(probs)/numOfPossibleHaps
	
def maximization_step(probabilities, hap_pairs):
	correct_pairs = []
	for i in range(len(probabilities)):
		index = np.argmax(probabilities[i])
		correct_pairs.append(hap_pairs[i][index])
	return correct_pairs

def em(filename, runs, piecesize):
	all_snps = phasing.loadfile(filename)
	answer = []
	i = 0
	while i < len(all_snps):
		hap_pairs = phasing.lst_haplotypes(all_snps[i:i+piecesize])
		haplotypes = phasing.remove_duplicates(hap_pairs)
		frequencies = {}
		for haplotype in haplotypes:
			frequencies[''.join(haplotype)] = 1/(len(haplotypes))
		for run in range(runs):
			frequencies, probabilities = expectation_step(haplotypes, hap_pairs, frequencies)
			best_haps = maximization_step(probabilities, hap_pairs)
			print("completed run # ",run)
		if i == 0:
			answer = best_haps
		else:
			for j in range(len(answer)):
				for k in range(len(answer[j])):
					answer[j][k].append(best_haps[j][k])
					answer[j][k] = list(chain.from_iterable(answer[j][k]))
		print("completed piece # ",i)
		i+= piecesize
	return answer
	
def output(final_haplotypes, output_file):
	haplotypes_flattened = list(chain.from_iterable(final_haplotypes))
	output_haplotypes = [[haplotypes_flattened[i][j] for i in range(len(haplotypes_flattened))] for j in range(len(haplotypes_flattened[0]))]
	file = open(output_file, 'w')
	for lst in output_haplotypes:
		for snp in lst:
			file.write(snp)
			file.write(' ')
		file.write('\n')
	return file

file1 = 'data/example_data_1.txt'
file2 = 'data/example_data_2.txt'
file3 = 'data/example_data_3.txt'

graded_file1 = 'data/test_data_1.txt'
graded_file2 = 'data/test_data_2.txt'

short_file = 'data/test.txt'

output_file_name = 'test_file.txt'

final_haplotypes = em(short_file, runs = 10, piecesize = 4)
output(final_haplotypes, output_file_name)