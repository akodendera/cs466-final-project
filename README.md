for CS 466 Final project

Dataset: ftp://ftp.ensembl.org/pub/release-96/fasta/chelonoidis_abingdonii/pep/Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa.gz 

Aiyappa Kodendera
Minhyuk Park

The datafile was too large for the git repository, so we did not include it here.
Need python3.6 to run. We have multi-processed program for the reading of the data and creation of graphs so this needs to be run on a system that supports fork.

The following are the python package dependencies you will need to run this: networkx, matplotlib, random, multiprocessing, , logging, pprint, Bio, and pandas

###To run ###
We have written a few testing functions in main.py. just run "python main.py" to run these