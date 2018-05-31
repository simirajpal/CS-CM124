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
    
    #sequentially assign haplotype based on neighbors
    snps = len(haplotypes)
    individuals = len(haplotypes[0])
    for i in range(snps):
        #look forward and behind 2 SNPs for probabilities
        begin = i - 1
        if begin < 0:
            begin = 0
        end = i + 2
        if end > snps:
            end = snps
        consideration = haplotypes[i]
        storage = []
        
        for p in range(begin, end):
            if p is not i:
                #get conditional probabilities
                temp = [[1,1][1,1]]
                conditional = haplotypes[p]
                for j in range(individuals):
                    if consideration[j] is '0':
                        if conditional[j] is '0':
                            temp[0][0] += 1
                        elif conditional is '1':
                            temp[0][1] += 1
                    elif consideration[j] is '1':
                        if conditional[j] is '0':
                            temp[1][0] += 1
                        elif conditional is '1':
                            temp[1][1] += 1
                
                #normalize values
                zero = sum(temp[0])
                one = sum(temp[1])
                temp[0][0] /= zero
                temp[0][1] /= zero
                temp[1][0] /= one
                temp[1][1] /= one
                storage.append(temp)
        
        for j in range(0,individuals,2):
            if j is 'x':
                
        
clarks('data/example_data_1.txt', 'data/example_data_1_geno_positions.txt')