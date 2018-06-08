"""
@author: Simi Rajpal

Haplotype Phasing for Recently Admixed Populations

"""

import phasing
import numpy as np
from itertools import chain
from collections import Counter

def expectation_step(haplotypes, hap_pairs, freq_lst):
    numGenotypes = len(hap_pairs)
    numHaplotypes = numGenotypes*2
    totalFrequencyValue = [sum([(freq_lst[pair[0]])*(freq_lst[pair[1]]) for pair in indiv]) for indiv in hap_pairs]        
    probabilities = [[find_probability(freq_lst[pair[0]], freq_lst[pair[1]], totalFrequencyValue[i]) for pair in indiv] for i, indiv in enumerate(hap_pairs)]
    frequencies = {}
    for haplotype in haplotypes:
        frequencies[haplotype] = find_frequency([probabilities[i][p] for i in range(numGenotypes) for p in range(len(hap_pairs[i])) if hap_pairs[i][p][0] == haplotype or hap_pairs[i][p][1] == haplotype], numHaplotypes)
    return frequencies, probabilities            

def find_probability(freq1, freq2, totalFrequencyValue):
    return (freq1*freq2)/totalFrequencyValue
    
def find_frequency(probs, numOfHaps):
    return sum(probs)/numOfHaps
    
def maximization_step(probabilities, hap_pairs):
<<<<<<< HEAD
    return [hap_pairs[i][np.argmax(probabilities[i])] for i in range(len(probabilities))]

def em(filename, runs, piecesize, remain):
    all_snps = phasing.loadfile(filename)
    inprogress = []
    answer = []
    mult = piecesize // remain
    lensnp = len(all_snps)
    i = 0
    while i < lensnp:
        hap_pairs = phasing.lst_haplotypes(all_snps[i:i+piecesize])
        haplotypes = phasing.remove_duplicates(hap_pairs)
        frequencies = {}
        for haplotype in haplotypes:
            frequencies[haplotype] = 1/(float(len(haplotypes)))
        for run in range(runs):
            frequencies, probabilities = expectation_step(haplotypes, hap_pairs, frequencies)
        
        best_haps = maximization_step(probabilities, hap_pairs)
        inprogress.append(best_haps)
        #if i == 0:
        #    answer = best_haps
        #else:
        #    for j in range(len(answer)):
        #        for k in range(len(answer[j])):
        #            answer[j][k] += best_haps[j][k]
                    #answer[j][k] = list(chain.from_iterable(answer[j][k]))
        #print("completed piece # ",i)
        i += remain

    #start off answer
    for b in inprogress[0]:
        answer.append([bb[:remain] for bb in b])
    for i in range(len(answer)):
        for j in range(2):
            for r in range(1, mult-1):
                answer[i][j] += inprogress[r][i][j][:remain]
    
    #add consensus into the answer
    compare = []
    edge = remain * (mult - 1)
    for index in range(edge, lensnp - edge, remain):
        seg = index // remain
        for i in range(len(answer)):
            for j in range(2):
            #wow = []
            #for m in range(mult):
                #wow.append(inprogress[seg - m][j][remain*m:remain*(m+1)])
                wow = [inprogress[seg - m][i][j][remain*m:remain*(m+1)] for m in range(mult)]
                compare = np.array(wow)
                compare = np.transpose(compare)
                e = [Counter(c).most_common(1)[0][0] for c in compare]
                answer[i][j] += ''.join(e)
    
    #finish up ends
    for i in range(len(answer)):
        for j in range(2):
            answer[i][j] += inprogress[-1 * (mult - 1)][i][j]

    return answer
    
	return [hap_pairs[i][np.argmax(probabilities[i])] for i in range(len(probabilities))]

def em(filename, runs, piecesize):
	all_snps = phasing.loadfile(filename)
	n = len(all_snps)
	answer = []
	i = 0
	while i < n:
		hap_pairs = phasing.lst_haplotypes(all_snps[i:i+piecesize])
		haplotypes = phasing.remove_duplicates(hap_pairs)
		frequencies = {}
		length = float(len(haplotypes))
		for haplotype in haplotypes:
			frequencies[haplotype] = 1/length
		for run in range(runs):
			frequencies, probabilities = expectation_step(haplotypes, hap_pairs, frequencies)
			best_haps = maximization_step(probabilities, hap_pairs)
		if i == 0:
			answer = best_haps
		else:
			for j in range(len(answer)):
				for k in range(len(answer[j])):
					answer[j][k] += best_haps[j][k]
					#answer[j][k] = list(chain.from_iterable(answer[j][k]))
		print("completed piece # ",i)
		i+= piecesize
	return answer
def output(final_haplotypes, output_file):
    haplotypes_flattened = list(chain.from_iterable(final_haplotypes))
    #haplotypes_flattened = final_haplotypes
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

output_file_name = 'finally.txt'

<<<<<<< HEAD
final_haplotypes = em(file1, runs = int(2), piecesize = int(4), remain = int(2))
=======
final_haplotypes = em(file1, runs = 3, piecesize = 12)
output(final_haplotypes, output_file_name)

'''from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graphviz = GraphvizOutput()
graphviz.output_file = 'check.png'

with PyCallGraph(output=graphviz):
    final_haplotypes = em(file1, runs = 4, piecesize = 8) 
    output(final_haplotypes, output_file_name)
'''