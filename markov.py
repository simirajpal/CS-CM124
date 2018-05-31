"""
@author: Linus Chen
"""

import phasing.py

#chance of crossover per base pair
R_PROB = 0.00000001

def load_cross_chance(filename):
    '''need the distance between SNPs to determine chance of crossover,
    which is used in the HMM for the transition probability.''' 
    cross = []
    with open(filename, 'r') as f:
        for line in f:
            cross.append(int(line))
    l = len(cross)
    print('number of snps: ' + str(l))
    for i in range(l-1, 0, -1):
        cross[i] = (cross[i] - cross[i-1])*R_PROB
    cross[0] = 0
    #if genome positions is empty, something is wrong
    if not cross:
        raise Exception('no genome positions')
    return cross

def initialize_markov(data_file, pos_file):
    '''unfinished as I don't know how to use the phasing.py
    load haplotype functions for markov'''
    cross = load_cross_chance(pos_file)
    #load data file into haplotypes
    haplotypes = []
    #go through haplotypes making initial markov estimates for each individual
    #should be a list (individuals) of lists (SNPs) of lists (haplotype states)
	phased_haps = lsthaplotypes(data_file) #list (individuals) of lists (haplotype states) of snps
    markov = []
    return cross, markov

def update_markov(markov_model, cross):
    '''markov_model is a list of of lists, where each list contains the 
    emission of a certain haplotype. There are n haplotype states, and possibly
    n additional "states" for the mutation chance?'''
    markov_model2 = []
    #j is the SNP, k is the state
    '''
    for j in range(len(markov_model)):
        states = []
        ll = len(j)
        for k in range(ll):
            for l in range(ll):
                other_states = sum([markov_model2[j-1][l] if l is not k]
            states.append(cross[j] * other_states + (1-cross[j]) * markov_model[j][k])
    '''
    return markov_model2

def markov(data_file,pos_file):
    cross, markov = initialize_markov(pos_file)
    markov2 = update_markov(markov, cross)
    return markov2

#markov('data/example_data_1_geno_positions.txt', 'data/example_data_1.txt')