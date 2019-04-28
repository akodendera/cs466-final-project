import pprint
from Bio import SeqIO
import pandas as pd
from tabulate import tabulate
pp = pprint.PrettyPrinter(indent=4)

filename = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'

df = pd.DataFrame()

sequence = SeqIO.parse(open(filename), 'fasta')
counter = 0
for record in sequence:
    df = df.append({
        'sequence_id': record.id,
        'sequence': str(record.seq)
    }, ignore_index=True)
    counter += 1
    if(counter % 10000 == 0):
        print(counter)

print(df.head)
print(tabulate(df, headers='keys', tablefmt='psql'))
