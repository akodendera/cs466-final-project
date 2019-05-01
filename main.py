from sequences import Sequences
from debruijingraph import *


N_THREADS = 20
FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
debroin = Sequences(N_THREADS, FILENAME)
print(debroin.df.shape[0])

threeMerGraphList = getGraphList(N_THREADS, debroin, 3)
print(len(threeMerGraphList))

s3 = "abccde"
g3 = DebruijinGraph(s3, 4)
g3.printGraph()

g3.find_naive_eulerian_path()
print("finding the eulerian path of {} using a naive greedy algorithm".format(s3))
print(repr(g3.naive_eulerian_path))

s4 = "0011101000"
g4 = DebruijinGraph(s4, 3)
g4.printGraph()

g4.find_naive_eulerian_path()
print("finding the eulerian path of {} using a naive greedy algorithm".format(s4))
print(repr(g4.naive_eulerian_path))