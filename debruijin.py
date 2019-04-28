from Bio import SeqIO

filename = 'Chelonoidis_abingdonii.ASM359739v1.pep.abinitio.fa'
sequence = SeqIO.parse(open(filename), 'fasta')

for record in sequence:
    print(record.id)
