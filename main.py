from sequences import Sequences
from debruijingraph import DebruijinGraph

# N_THREADS = 20
# FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
# debroin = Sequences(N_THREADS, FILENAME)
# print(debroin.df.shape[0])

# s2 = debroin.df['sequence'].iloc[0]
# g2 = makeDebruijinGraph(s2, 3)
# g2.printGraph()
# three_mer_graph_list = []
# for i in range(debroin.df.shape[0]):
# for i in range(200):
#     s = debroin.df['sequence'].iloc[i]
#     three_mer_graph_list.append(DebruijinGraph(s, 3))

s3 = "abccde"
g3 = DebruijinGraph(s3, 4)
g3.printGraph()

g3.find_naive_eulerian_path()
print(repr(g3.naive_eulerian_path))

s4 = "0011101000"
g4 = DebruijinGraph(s4, 3)
g4.printGraph()

g4.find_naive_eulerian_path()
print(repr(g4.naive_eulerian_path))
