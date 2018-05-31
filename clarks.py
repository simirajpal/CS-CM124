import csv
from markov.py import load_cross_chance, R_PROB


def clarks(datafile,posfile):
    cross = load_cross_chance(posfile)
    haplotypes = []
    with open(datafile, 'r') as f:
        filereader = csv.reader(f. delimiter=' ')
        for row in filereader:
            temp = []
            for r in row:
                if r is '0':
                    temp.extend('0','0')
                elif r is '2':
                    temp.extend('1','1')
                else:
                    temp.extend('x','x')
            if not temp:
                raise Exception('no temp')
            haplotypes.append(temp)
    if not haplotypes:
        raise Exception('no haplotypes')
    
    for row in haplotypes:
        
clarks('data/example_data_1.txt', 'data/example_data_1_geno_positions.txt')