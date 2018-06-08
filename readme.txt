first, make sure anaconda for python3-4.2 is available.
for hoffman2, run:
	module load anaconda/python3-4.2

to test the datasets, run these from the folder with em.py:
	python3 ./em.py data/test_data_1.txt 4 9 3 test_data_1_sol.txt
	python3 ./em.py data/test_data_2.txt 4 9 3 test_data_2_sol.txt