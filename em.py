"""
@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""

import phasing.py
import numpy as np

# freq_lst needs to be a dictionary
def expectation_step(haplotypes, hap_pairs, freq_lst):
	probabilities = []
	for i in range(len(hap_pairs)):
		prob = []
		for p in range(len(hap_pairs[i])):
			f1 = freq_lst[hap_pairs[i][p][0]]
			f2 = freq_lst[hap_pairs[i][p][1]]
			probability.append(find_probabaility(f1, f2, len(hap_pairs[i])))
		probabilities.append(probability)
	frequencies = []	
	for haplotype in haplotypes:
		probs = []
		for j in range(len(hap_pairs)):
			for q in range(len(hap_pairs[j])):
				if hap_pairs[j][q][0] == haplotype or hap_pairs[j][q][1] == haplotype:
					probs.append(probability[j][q])
		frequencies.append(find_frequency(probs, len(haplotypes)))
	return frequencies, probabilities			

def find_probability(freq1, freq2, numOfPairs):
	return (freq1*freq2)/(numOfPairs(freq1+freq2))
	
def find_frequency(probs, numOfPossibleHaps):
	return sum(probs)/numOfPossibleHaps
	
def maximization_step(frequencies, probabilities, hap_pairs):
	correct_pairs = []
	for i in range(len(probabilities)):
		index = np.argmax(probabilities[i])
		correct_pairs.append(hap_pairs[i][index])
	return correct_pairs

def em(filename, runs):
	haplotypes = lst_haplotypes((loadfile(filename)))
	hap_pairs = remove_duplicates(haplotypes)
	frequencies = [1/(len(haplotypes)) for haplotype in haplotypes]
	for run in runs:
		frequencies, probabilities = expectation_step(haplotypes, hap_pairs, frequencies)
		answer = maximization_step(frequencies, probabilities, hap_pairs)
	return answer
	

print(em("data/test.txt", 2))
			