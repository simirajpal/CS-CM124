"""
@author: Simi Rajpal, Linus Chen

Haplotype Phasing for Recently Admixed Populations

arguments: input file, iteration count, piece size, increment, output file
"""

import phasing
import numpy as np
import sys
from itertools import chain
from collections import Counter,defaultdict

def em_step(haplotypes, hap_pairs, numGenotypes, freq_lst):
    #numGenotypes = len(hap_pairs)
    numHaplotypes = numGenotypes*2
    frequencies = [[(freq_lst[pair[0]])*(freq_lst[pair[1]]) for pair in indiv] for indiv in hap_pairs]
    #totalFrequencyValue = [sum(f) for f in frequencies]        
    #probabilities = [[find_probability(freq_lst[pair[0]], freq_lst[pair[1]], totalFrequencyValue[i]) for pair in indiv] for i, indiv in enumerate(hap_pairs)]
    probabilities = []
    
    for f in frequencies:
        totalFrequency = sum(f)
        temp = [freq/totalFrequency for freq in f]
        probabilities.append(temp)
    
    frequencies = defaultdict(lambda: 0)
    #for haplotype in haplotypes:
    for i in range(numGenotypes):
        for p in range(len(hap_pairs[i])):
            haplotype1 = hap_pairs[i][p][0]
            haplotype2 = hap_pairs[i][p][1]
            prob = probabilities[i][p]
            frequencies[haplotype1] = frequencies[haplotype1] + prob
            frequencies[haplotype2] = frequencies[haplotype2] + prob
        #oh = [probabilities[i][p] for i in range(numGenotypes) for p in range(len(hap_pairs[i])) if hap_pairs[i][p][0] == haplotype or hap_pairs[i][p][1] == haplotype]
        #frequencies[haplotype] = find_frequency(oh, numHaplotypes)
    
    for haplotype in haplotypes:
        frequencies[haplotype] /= numHaplotypes 
    
    return frequencies, probabilities            

def find_probability(freq1, freq2, totalFrequencyValue):
    return (freq1*freq2)/totalFrequencyValue
    
def find_frequency(probs, numOfHaps):
    return sum(probs)/numOfHaps
    
def best(probabilities, hap_pairs):
    return [hap_pairs[i][np.argmax(probabilities[i])] for i in range(len(probabilities))]

def em(filename, runs, piecesize, remain):
    all_snps = phasing.loadfile(filename)
    inprogress = []
    answer = []
    mult = piecesize // remain
    lensnp = len(all_snps)
    numGenotypes = len(all_snps[0])
    i = 0
    while i < lensnp:
        hap_pairs = phasing.lst_haplotypes(all_snps[i:i+piecesize])
        haplotypes = phasing.remove_duplicates(hap_pairs)
        haplotypes = [''.join(h) for h in haplotypes]
        frequencies = {}
        const = 1/(float(len(haplotypes)))
        for haplotype in haplotypes:
            frequencies[haplotype] = const
        for run in range(runs):
            frequencies, probabilities = em_step(haplotypes, hap_pairs, numGenotypes, frequencies)
        
        best_haps = best(probabilities, hap_pairs)
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
        answer.append([b[0][:remain], b[1][:remain]])
    for i in range(len(answer)):
        for j in range(2):
            for r in range(1, mult-1):
                answer[i][j] += inprogress[r][i][j][:remain]
    
    #add consensus into the answer
    edge = remain * (mult - 1)
    for index in range(edge, lensnp - edge, remain):
        seg = index // remain
        for i in range(len(answer)):
            for j in range(2):
            #wow = []
            #for m in range(mult):
                #wow.append(inprogress[seg - m][j][remain*m:remain*(m+1)])
                wow = [inprogress[seg - m][i][j][remain*m:remain*(m+1)] for m in range(mult)]
                compare = [[wow[j][i] for j in range(mult)] for i in range(remain)]
                e = [Counter(c).most_common(1)[0][0] for c in compare]
                answer[i][j] += ''.join(e)
    
    #finish up ends
    for i in range(len(answer)):
        for j in range(2):
            answer[i][j] += inprogress[-1 * (mult - 1)][i][j]

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

output_file_name = 'output_example_data_1.txt'

final_haplotypes = em(sys.argv[1], runs = int(sys.argv[2]), piecesize = int(sys.argv[3]), remain = int(sys.argv[4]))
output(final_haplotypes, sys.argv[5])
