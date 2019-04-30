from sequences import Sequences
from debruijingraph import DebruijinGraph

N_THREADS = 20
FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
debroin = Sequences(N_THREADS, FILENAME)
print(debroin.df.shape[0])

# s2 = debroin.df['sequence'].iloc[0]
# g2 = makeDebruijinGraph(s2, 3)
# g2.printGraph()
three_mer_graph_list = []
# for i in range(debroin.df.shape[0]):
for i in range(200):
    s = debroin.df['sequence'].iloc[i]
    three_mer_graph_list.append(DebruijinGraph(s, 3))

print len(three_mer_graph_list)