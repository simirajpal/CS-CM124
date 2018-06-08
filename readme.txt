first, make sure anaconda for python3-4.2 is available.
for hoffman2, run:
	module load anaconda/python3-4.2

make sure the datasets are in a folder called data and make sure em.py, phasing.py, and the folder data are in the same directory
to test the datasets, run these from the directory with em.py 
	python3 ./em.py data/test_data_1.txt 4 12 4 test_data_1_sol.txt
	python3 ./em.py data/test_data_2.txt 4 12 4 test_data_2_sol.txt