from sequences import Sequences
from debruijingraph import DebruijinGraph

N_THREADS = 20
FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
debroin = Sequences(N_THREADS, FILENAME)
print(debroin.df.shape[0])

# s2 = debroin.df['sequence'].iloc[0]
# g2 = makeDebruijinGraph(s2, 3)
# g2.printGraph()



