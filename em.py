"""
@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""

import phasing
import numpy as np

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

def em(filename, runs):
	hap_pairs = phasing.lst_haplotypes((phasing.loadfile(filename)))
	haplotypes = phasing.remove_duplicates(hap_pairs)
	frequencies = {}
	for haplotype in haplotypes:
		frequencies[''.join(haplotype)] = 1/(len(haplotypes))
	for run in range(runs):
		frequencies, probabilities = expectation_step(haplotypes, hap_pairs, frequencies)
		answer = maximization_step(probabilities, hap_pairs)
	return answer
	

print(em("data/test.txt", 10))
			