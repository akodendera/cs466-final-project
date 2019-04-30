from debruijin import DeBruijn
from naivedebruijn import *

s = "abcdefgcdadem"
g = makeDebruijinGraph(s, 3)
g.printGraph()

N_THREADS = 20
FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
debroin = DeBruijn(N_THREADS, FILENAME)
print(debroin.df.shape)

s2 = debroin.df['sequence'].iloc[0]
g2 = makeDebruijinGraph(s2, 3)
g2.printGraph()
