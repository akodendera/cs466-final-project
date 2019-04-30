from debruijin import DeBruijn

N_THREADS = 20
FILENAME = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
debroin = DeBruijn(N_THREADS, FILENAME)
print(debroin.df.shape)
